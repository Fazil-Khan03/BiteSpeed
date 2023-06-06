This Readme provides instructions on how to set up a local development environment for a Django project using SQLite as the database and Python as the programming language.

Prerequisites
Before proceeding with the setup, ensure that you have the following installed on your system:

Python 3.x (https://www.python.org/downloads/)
pip (https://pip.pypa.io/en/stable/installing/)
Django (https://www.djangoproject.com/download/)
SQLite (https://www.sqlite.org/download.html)

Getting Started
Clone the project repository or download the source code.

Create a virtual environment for your project (optional but recommended):



$ python3 -m venv myenv
$ source myenv/bin/activate  # On Windows: myenv\Scripts\activate


Install project dependencies:
$ pip install -r requirements.txt


Django uses SQLite as the default database backend. To create a new SQLite database file, run the following command:


$ python manage.py migrate
This command will create the necessary tables for the project.

Run the development server:

$ python manage.py runserver

Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
Access the application:
Open your web browser and navigate to http://127.0.0.1:8000/ to access the locally running Django application.

Additional Configuration

Database Configuration
By default, Django uses the SQLite database configuration in the project's settings. However, if you want to change the database settings or use a different database, you can modify the settings.py file in your Django project directory.

Example settings.py configuration using SQLite:

python
Copy code
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


Admin Interface
Django provides an admin interface for managing the application's data. To access the admin interface, you need to create a superuser account:


$ python manage.py createsuperuser
Follow the prompts to enter the desired username and password.

You can then access the admin interface at http://127.0.0.1:8000/admin/ and log in using the superuser account credentials.

Conclusion
You have now successfully set up a local development environment for your Django project using SQLite as the database and Python as the programming language. Feel free to explore and customize the project according to your requirements.

For more information on Django and its features, refer to the official Django documentation.

Url Endpoint
POST API : 0.0.0.0:800X/identity/
