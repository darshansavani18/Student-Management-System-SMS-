# Student Management System

A web-based student management system built with Django. This application allows administrators to manage students and teachers, including adding, viewing, updating, and deleting student records, as well as adding teachers.

## Features

- **User Authentication**: Login and logout functionality for secure access.
- **Dashboard**: Overview displaying total number of students and teachers.
- **Student Management**:
  - Add new students with details like roll number, class, section, gender, date of birth, and address.
  - View all students with search functionality (by username, roll number, or class).
  - Update student information.
  - Delete students (including associated user accounts).
- **Teacher Management**:
  - Add new teachers with details like full name, email, subject, and phone number.
- **Responsive Design**: Uses CSS for a clean and user-friendly interface.

## Technology Stack

- **Backend**: Django 6.0
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS
- **Authentication**: Django's built-in authentication system

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/darshansavani18/student-management-system.git
   cd student-management-system
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv env


   
   # On Windows:
   env\Scripts\activate



   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   Open your browser and go to `http://127.0.0.1:8000/`

## Usage

- Log in using your credentials.
- Navigate to the dashboard to see an overview.
- Use the menu to add students/teachers, view students, etc.
- Search for students by entering queries in the search box on the view students page.

## Project Structure

```
student-management-system/
├── home/                 # Main Django project directory
│   ├── settings.py       # Project settings
│   ├── urls.py           # Main URL configuration
│   └── ...
├── school/               # Django app for school management
│   ├── models.py         # Database models (Student, Teacher)
│   ├── views.py          # View functions
│   ├── forms.py          # Django forms
│   ├── urls.py           # App URL configuration
│   └── ...
├── templates/            # HTML templates
│   └── school/
├── static/               # Static files (CSS, JS)
│   └── school/
├── db.sqlite3            # SQLite database
└── manage.py             # Django management script
```

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
