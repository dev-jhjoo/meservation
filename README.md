# Introduction
This is a toy project for learning Django. The project name, Meservation, is a combination of 'me' and 'reservation'.

## Prerequisites
Before you begin, ensure you have the following MySQL environment variables set. These are used for connecting to your MySQL database.

```bash
export DB_NAME=<your_database_name>  # The name of your MySQL database
export DB_USER=<your_database_user>  # The user that will connect to the MySQL database
export DB_PASSWORD=<your_database_password>  # The password of the user
export DB_HOST=<your_database_host>  # The host of your MySQL database, usually localhost if the database is on your machine
export DB_PORT=<your_database_port>  # The port to connect to your MySQL database
```

# Installation
```bash
pip install -r requirements.txt
```

# Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

# Usage
```bash
python manage.py runserver
```

You can now access the Meservation project from your web browser at http://localhost:8000.
