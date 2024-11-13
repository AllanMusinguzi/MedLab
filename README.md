
# MedLab

**MedLab** is an offline desktop application built with Tkinter to manage laboratory operations. It simplifies and streamlines processes such as patient management, test management, and result tracking, enhancing workflow efficiency for medical laboratories even without an internet connection.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Packaging](#packaging)
7. [Contributing](#contributing)
8. [License](#license)

---

## Features

- **Patient Management**: Add, update, and retrieve patient details.
- **Test Management**: Organize test types, samples, and track their statuses.
- **Result Management**: Record and access test results for patients.
- **User Roles and Permissions**: Supports different roles (Admin, Super Admin, User) with role-specific access control.
- **Report Generation**: Generate and download reports for patient records and test results.
- **Offline Operation**: Operates independently of the internet, ideal for low-connectivity areas.

---

## Project Structure

The project files are organized as follows:

```
MedLab/
├── __pycache__/                 # Python cache files
├── .vscode/                     # VSCode configuration files
├── backups/                     # Backups and data files
├── build/                       # Build output for the application
├── dist/                        # Distribution files for packaging
├── Downloads/                   # Temporary downloads folder
├── icons/                       # Application icons and other images
├── Modules/                     # Main modules of the application
│   ├── adminModule/             # Admin-related functionalities
│   ├── loginSignup/             # Login and signup functionalities
│   ├── superAdminModule/        # Super Admin-specific functionalities
│   └── usersModule/             # User-related functionalities
├── myenv/                       # Virtual environment for dependencies
├── uploads/                     # Directory for uploaded files
├── config.ini                   # Configuration file with app settings
├── main.py                      # Main application script
├── main.spec                    # PyInstaller spec file for packaging
└── report_generate.py           # Script for generating reports
```

---

## Installation

### Prerequisites

- Python 3.x
- `pip` package manager

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/AllanMusinguzi/MedLab.git
   cd MedLab
   ```

2. **Set Up Virtual Environment** (recommended):

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Application**:

   Edit the `config.ini` file to adjust settings such as database path and other configurations as needed.

---

## Configuration

The `config.ini` file is used for application configurations, such as:

- Database settings
- File storage paths
- Other app-specific settings

Update this file according to your environment and requirements.

---

## Usage

1. **Run the Application**:

   Start the app using:

   ```bash
   python main.py
   ```

2. **Navigate**: 

   - Log in or register based on user role.
   - Access patient management, test management, results, and report generation features from the app interface.

---

## Packaging

To create a standalone executable, use **PyInstaller** with the provided `main.spec` file:

```bash
pyinstaller main.spec
```

This command will create an executable in the `dist/` folder, which can be distributed and run on other systems.

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Submit a pull request with a description of your changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

---

This README file should provide clear, organized information to users and contributors of MedLab. Let me know if there are additional sections you'd like to include!
