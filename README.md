Medical Lab Management System
Table of Contents

    Project Description
    Features
    System Requirements
    Installation
    Database Configuration
    Usage
    Login Credentials
    Technologies Used
    License

Project Description

The Medical Lab Management System is designed to simplify and automate the management of medical laboratory operations. It allows administrators and users to manage patient records, test results, and laboratory activities seamlessly. The system provides role-based access for both admins and users, ensuring secure management of sensitive data.
Features

    User Authentication: Admin and user login functionalities with secure password hashing.
    Role-based Access Control: Admins have full access to the system, while users have limited access based on their role.
    Manage Patient Records: Admins can add, update, and delete patient records.
    Test Management: Manage and record medical test results for patients.
    Reporting: Generate reports based on test results and patient history.
    Error Handling: Provides user-friendly error messages for common issues during login and other operations.

System Requirements

Before running the Medical Lab Management System, ensure your machine meets the following requirements:

    Operating System: Ubuntu (Linux) or any Linux-based distribution
    Python Version: Python 3.x
    Database: MySQL or MariaDB (set up via XAMPP or Docker)
    Libraries/Frameworks: Listed in requirements.txt

Installation

  Clone the Repository:
    git clone https://github.com/your-username/medical-lab-management.git
    cd medical-lab-management
    
  Create a Virtual Environment (optional but recommended):
    python3 -m venv venv
    source venv/bin/activate

  Install Dependencies: Install all required Python packages using pip:
    pip install -r requirements.txt

  Configure MySQL Database: Make sure MySQL (or MariaDB) is running, and create a database for the system:
    CREATE DATABASE medical_lab_db;

Database Configuration

  Modify the database configuration in your project to connect to the newly created database:
    Update the database connection details in the relevant configuration file (e.g., config.py or .env):
      DATABASE_HOST = 'localhost'
      DATABASE_USER = 'root'
      DATABASE_PASSWORD = 'your_password'
      DATABASE_NAME = 'medical_lab_db'
      
  Run Database Migrations (if applicable):
      python manage.py migrate


Usage

    Run the Application:
      python app.py
    Login to the system with the following credentials:
        Admin: Use the admin username and password set during registration.
        User: Use the user credentials provided during the user creation process.

    Access the Admin Panel: Once logged in as an admin, you will have access to add patients, update records, manage test results, and generate reports.

    Login Credentials

    You can use the following login credentials for testing purposes:

        Admin:
            Username: admin
            Password: admin123
    
        User:
            Username: user
            Password: user123

    Make sure to replace these credentials with more secure ones for production use.
    
Technologies Used

    The Medical Lab Management System is built using the following technologies:
    
        Frontend: Tkinter (for GUI)
        Backend: Python 3, Flask (or another backend framework if applicable)
        Database: MySQL or MariaDB
        Libraries:
            bcrypt (for password hashing)
            MySQL connector (for database interaction)

License

    This project is licensed under the MIT License.
