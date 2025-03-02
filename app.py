from flask import Flask, render_template, redirect, url_for, request, flash, session 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate 
from config import Config
from models import db, User, FoodDonation, DonationRequest
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)
  
@app.route('/update_status/<int:donation_id>', methods=['POST'])
def update_status(donation_id):
    # Check if the user is logged in and has the correct role
    if 'user_id' not in session:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('login'))

    if session.get('role') != 'host':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('dashboard'))

    donation = FoodDonation.query.get_or_404(donation_id)
    new_status = request.form.get('status')
    
    if new_status not in ['available', 'requested', 'donated']:
        flash("Invalid status.", "danger")
        return redirect(url_for('dashboard'))

    if new_status == 'donated':
        # If the status is "donated", delete the donation from the database
        db.session.delete(donation)
        db.session.commit()
        
    else:
        # Update the status in the database
        donation.status = new_status
        db.session.commit()
        

    # Redirect back to the dashboard for the host
    return redirect(url_for('dashboard'))


    
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        role = request.form['role']
        new_user = User(username=username, password=password, email=email, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if session['role'] == 'host':
        donations = FoodDonation.query.filter_by(host_id=session['user_id']).all()
        return render_template('dashboard.html', donations=donations)

    elif session['role'] == 'charity':
        donations = FoodDonation.query.filter_by(status="available").all()
        cities = [d.city for d in FoodDonation.query.distinct(FoodDonation.city)]
        hosts = User.query.filter_by(role="host").all()
        return render_template('donations.html', donations=donations, hosts=hosts, cities=cities)

@app.route('/add_donation', methods=['POST'])
def add_donation():
    if session.get('role') == 'host':
        food_type = request.form['food_type']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']
        city = request.form['city']
        new_donation = FoodDonation(
            host_id=session['user_id'], food_type=food_type,
            quantity=quantity, expiration_date=expiration_date, city=city
        )
        db.session.add(new_donation)
        db.session.commit()
        flash('Donation added successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/filter_donations', methods=['GET'])
def filter_donations():
    if 'user_id' not in session or session['role'] != 'charity':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('login'))

    # Retrieve distinct cities and sort them alphabetically
    unique_cities = sorted([row[0] for row in db.session.query(FoodDonation.city).distinct()])

    # Retrieve all hosts
    hosts = User.query.filter_by(role="host").all()

    # Get filter parameters
    city = request.args.get('city')
    host_id = request.args.get('host_id')

    # Filter donations based on city and host
    query = FoodDonation.query.filter_by(status="available")
    if city:
        query = query.filter_by(city=city)
    if host_id:
        query = query.filter_by(host_id=host_id)

    # Fetch filtered donations
    donations = query.all()

    return render_template('donations.html', donations=donations, cities=unique_cities, hosts=hosts)

@app.route('/request_donation/<int:donation_id>', methods=['POST'])
def request_donation(donation_id):
    if session.get('role') == 'charity':
        donation = FoodDonation.query.get_or_404(donation_id)

        # Ensure the donation is available before requesting
        if donation.status != "available":
            flash("This donation is no longer available.", "danger")
            return redirect(url_for('dashboard'))

        new_request = DonationRequest(charity_id=session['user_id'], donation_id=donation_id)
        donation.status = "requested"
        db.session.add(new_request)
        db.session.commit()

        flash('Donation request submitted!', 'success')
    else:
        flash("Unauthorized access.", "danger")
    return redirect(url_for('dashboard'))


@app.route('/donation_history')
def history():
    if 'user_id' not in session:
        flash("Please log in to view the history.", "danger")
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    if role == "host":
        donations = FoodDonation.query.filter_by(host_id=user_id).all()
    elif role == "charity":
        donations = db.session.query(
            FoodDonation, DonationRequest, User.username
        ).join(DonationRequest, FoodDonation.id == DonationRequest.donation_id)\
        .join(User, FoodDonation.host_id == User.id)\
        .filter(DonationRequest.charity_id == user_id).all()
    else:
        donations = []

    return render_template('donation_history.html', donations=donations, role=role)


@app.template_filter('date')
def format_date(value, format='%Y-%m-%d'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

@app.route('/delete_donation/<int:donation_id>', methods=['POST'])
def delete_donation(donation_id):
    if session.get('role') == 'host':
        donation = FoodDonation.query.get_or_404(donation_id)

        # Delete dependent rows in DonationRequest
        DonationRequest.query.filter_by(donation_id=donation_id).delete()

        # Delete the donation itself
        db.session.delete(donation)
        db.session.commit()
        flash("Donation deleted successfully!", "success")
    else:
        flash("Unauthorized access.", "danger")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)