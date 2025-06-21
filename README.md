Food Donation Platform
Connecting wedding hosts with charities to reduce food waste and support communities in need.
The Food Donation Platform is a sophisticated web application built with Flask and MySQL, designed to streamline the process of donating surplus food from events like weddings to charitable organizations. This platform empowers wedding hosts to register and manage food donations while enabling charities to request and track available donations efficiently. With a modern, responsive UI and robust backend, it ensures seamless user interactions and secure data management.
✨ Key Features

Role-Based Access Control:
Wedding Hosts: Register and manage food donations, update donation statuses (Available, Requested, Donated), and delete donations.
Charity Organizers: Browse available donations, filter by city or host, request donations, and view donation history.


Dynamic Donation Management:
Add donations with details like food type, quantity, expiration date, and city.
Update donation statuses, with automatic deletion when marked as "Donated."
Filter donations by city and host for targeted charity searches.


Secure Authentication:
User registration with password hashing using Werkzeug.security`.
Session-based login/logout with role validation.
Password visibility toggle and client-side password validation (minimum 8 characters).


Responsive UI:
Modern, mobile-friendly design with Tailwind CSS-inspired styles.
Background image integration for a visually appealing experience.
Accessible tables with ARIA labels for improved usability.


Database Management:
MySQL database with Flask-SQLAlchemy for efficient data modeling.
Models for Users, Food Donations, and Donation Requests with foreign key constraints.
Flask-Migrate for seamless database schema updates.


Flash Messaging:
User feedback for actions like registration, login errors, and donation updates.


Donation History:
Comprehensive history tracking for both hosts and charities, with role-specific views.


Customizable Filters: Allows charities to filter donations by city or wedding organizer, improving usability.
Data Integrity: Ensures donation requests are only made for available donations, with cascading deletes for dependent records.

🛠️ Tech Stack

Backend: Python, Flask, Flask-SQLAlchemy, Flask-Migrate, Werkzeug
Database: MySQL (via mysql-connector-python)
Frontend: HTML, CSS (Custom styles with Tailwind-inspired design), JavaScript
Dependencies: Listed in requirements.txt for easy setup
Deployment: Configurable via environment variables (e.g., SECRET_KEY)

🚀 Getting Started
Prerequisites

Python 3.8+
MySQL Server (configured with a database named charity_db)
Git (for cloning the repository)

Installation

Clone the Repository:
git clone https://github.com/your-username/food-donation-platform.git
cd food-donation-platform


Set Up a Virtual Environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt


Configure Environment Variables:

Create a .env file in the project root or set the following environment variable:export SECRET_KEY="your-secret-key"  # On Windows: set SECRET_KEY=your-secret-key


Update config.py with your MySQL credentials if different:SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://<username>:<password>@localhost/charity_db"




Initialize the Database:
flask db init
flask db migrate -m "Initial migration"
flask db upgrade


Run the Application:
python app.py


Access the app at http://localhost:5000.



Directory Structure
food-donation-platform/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # Database models
├── requirements.txt        # Project dependencies
├── static/                 # Static files (CSS, images)
│   ├── style.css           # Custom styles
│   └── charity.jpg         # Background image
├── templates/              # HTML templates
│   ├── dashboard.html       # Host dashboard
│   ├── donations.html       # Charity donation view
│   ├── donation_history.html# Donation history
│   ├── login.html           # Login page
│   └── register.html        # Registration page
├── migrations/             # Database migration files
└── README.md               # Project documentation

📖 Usage

Register:

Navigate to /register and create an account as a "Wedding Host" or "Charity Organizer."
Passwords must be at least 8 characters long.


Login:

Use /login to access your dashboard based on your role.


For Wedding Hosts:

Add new donations via the dashboard form.
Update donation statuses or delete donations as needed.


For Charity Organizers:

Browse available donations at /dashboard.
Filter by city or host and request available donations.
View your donation history at /donation_history.


Logout:

Use the logout link to end your session securely.



🧪 Testing
To test the application:

Ensure MySQL is running and the database is set up.
Run the app in debug mode (app.run(debug=True)).
Use tools like Postman to test API endpoints (e.g., /add_donation, /request_donation).
Manually verify UI interactions for registration, login, and donation management.

🔮 Future Enhancements

Email Notifications: Send confirmation emails for donation requests and status updates.
Advanced Filters: Add more filtering options (e.g., food type, expiration date range).
User Profiles: Allow users to update their profiles and add contact details.
Analytics Dashboard: Provide insights into donation trends for hosts and charities.
Multi-Language Support: Localize the platform for broader accessibility.
API Endpoints: Expose RESTful APIs for third-party integrations.

🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

Please follow the Code of Conduct and ensure tests pass before submitting.
📝 License
This project is licensed under the MIT License.
🙌 Acknowledgments

Flask and SQLAlchemy communities for robust frameworks.
Tailwind CSS for UI inspiration.
MySQL for reliable database management.


🌟 Star this repository if you find it useful! For questions or feedback, open an issue or contact the maintainer at [balanansh123@gmail.com].
