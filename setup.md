Setting Up and Running the Bank Reporting System 🚀
Prerequisites 📋

Before you begin, ensure you have the following installed:

    Docker
    Docker Compose
    Git (for cloning the repository)

Initial Setup 🛠️

    Clone the Repository:

    bash

git clone [Your Repository URL]
cd [Your Project Directory]

Environment Variables:

    Copy the .env.sample file to a new file named .env.
    Modify the .env file to include your specific settings such as DB_NAME, DB_USER, DB_PASS, and SECRET_KEY.

Build Docker Containers:

bash

    docker-compose build

    This command builds the images for your application and its services.

Running the Application 🌐

    Start the Containers:

    bash

    docker-compose up

    This command starts all the services defined in your docker-compose.yml file.

    Accessing the Application:
        The Django application will be accessible at http://localhost (or another specified port in your docker-compose file).
        Access the Django admin panel at http://localhost/admin.

Managing the Database 🗃️

    Migrations:
        To apply database migrations, use:

        bash

    docker-compose exec [Your Django Service Name] python manage.py migrate

Creating a Superuser:

    To create an admin user, run:

    bash

        docker-compose exec [Your Django Service Name] python manage.py createsuperuser

Additional Commands 🧰

    Stopping the Application:

    bash

docker-compose down

Viewing Logs:

bash

docker-compose logs

Rebuilding Containers After Changes:

bash

    docker-compose build

Troubleshooting 🛠️

    If you encounter issues, check the Docker logs for error messages.
    Ensure that all environment variables in the .env file are correctly set.
    Verify that Docker and Docker Compose are properly installed and updated.