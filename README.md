# UniSafe Backend

## Prerequisites

Before you begin, ensure you have met the following requirements for the Django backend:

- **Python**: The project requires Python 3.8 or newer. Ensure you have the correct version of Python installed on your system.

- **PostgreSQL**: This project uses PostgreSQL. Ensure you have PostgreSQL version 12 or newer installed and running on your system.

- **Virtual Environment**: It's recommended to use a virtual environment for Python projects to manage dependencies.

- **Dependencies**: Install all the dependencies listed in your `requirements.txt`.

Ensure these prerequisites are met to successfully set up and run the Django backend of your application.

## Setup

1. **Clone the repository:**

```bash
   git clone https://github.com/FYP-UniSafe/UniSafe_Backend.git
```

2. **Create and Activate the virtual env:**

```bash
    python -m venv env && source env/bin/activate
```

3. **Install the development dependencies:**

```bash
    pip install -r requirements/dev.txt
```

4. **Configure Pre-commit (Optional):**

```bash
    pre-commit install && pre-commit run --all-files
```

5. **Navigate to the project directory:**

```bash
    cd Unisafe
```

6. **Apply Migrations:**

```bash
    python manage.py migrate
```

7. **Create a superuser:**

```bash
    python manage.py createsuperuser
```

8. **Run the development server:**

```bash
    python manage.py runserver
```

9. **Open your browser and navigate to `http://localhost:8000/` to view the application and view the `OpenAPI` swagger docs.**

## Setting Up Postgres on Django Project

To set up PostgreSQL on a Linux system, you will need to do the following steps:

1. **Install the PostgreSQL package:**

```bash
sudo apt-get install postgresql postgresql-contrib
```

2. **Start the PostgreSQL service:**

```bash
sudo service postgresql start
```

3. **Log in to the PostgreSQL command-line interface as the postgres user:**

```bash
sudo -u postgres psql
```

4. **Create a new database and user:**

```bash
CREATE DATABASE yourdatabasename;

CREATE USER youruser WITH PASSWORD 'yourpassword';

GRANT ALL PRIVILEGES ON DATABASE yourdatabasename TO youruser;
```

> **Note**: Dont use the username `user` as it will conflict with the command

5. **Exit the PostgreSQL command-line interface:**

```bash
\q
```

6. **Update the Django settings to use the new database:**

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdatabasename',
        'USER': 'youruser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

By following these steps, you should be able to set up PostgreSQL on your Linux system and use it with Django.
