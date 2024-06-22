# Expense Tracker

This is a Django-based web application for tracking personal expenses. Users can add, manage, and view expenses, set budget limits, and generate reports. The application also supports multi-currency expenses and provides basic authentication and authorization functionalities.

<table>
  <tr>
    <td><img src="./Expense tracker/1.png" alt="Expense Tracker" style="width: 400px; height: 300px"></td>
    <td><img src="./Expense tracker/2.png" alt="Expense Tracker" style="width: 400px; height: 300px"></td>
  </tr>
  <tr>
    <td><img src="./Expense tracker/3.png" alt="Expense Tracker" style="width: 400px; height: 300px"></td>
    <td><img src="./Expense tracker/4.png" alt="Expense Tracker" style="width: 400px; height: 300px"></td>
  </tr>
</table>

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Description

The Expense Tracker application allows users to efficiently manage their personal finances. Users can add expenses, categorize them, set budget limits for different categories, and view detailed reports of their spending habits. The application supports multiple currencies and can convert expenses to a base currency for easy comparison. It also includes user authentication and role-based access control.

## Installation

1. Ensure you have Python and Django installed on your system.
2. Clone the repository:

```sh
git clone https://github.com/aFro95/expense-tracker.git
```
3. Navigate to the project directory:

```sh
cd expense-tracker
```

4. Install the required dependencies:

```sh
pip install -r requirements.txt
```

5. Apply migrations to set up the database:

```sh
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser account:

```sh
python manage.py createsuperuser
```

7. Run the development server:

```sh
python manage.py runserver
```

## Usage
1. Open your web browser and navigate to http://127.0.0.1:8000/.
2. Register a new user account or log in with the superuser account you created.
3. Use the navigation menu to add expenses, set budget limits, and view reports.
4. Manage categories and other settings through the admin interface at http://127.0.0.1:8000/admin/.

## License
This project is licensed under the MIT License.
