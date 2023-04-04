# medexer-api
API for Medexer Limited built with django-rest-framework

# How to use
  - Clone the application onto your computer and change directory into it
  - Create a python virtual environment in the project directory and activate it
  - Install the projects dependencies with "pip install -r requirements.txt"
  - Create a ".env" file in the root directory of the project and copy the contents of the .env_example into it (PS you will need to install postgresql database on your local machine)
  - Make migrations with "python3 manage.py makemigrations"
  - Run the migrations with "python3 manage.py migrate"
  - Run the application with "python3 manage.py runserver"
  - Lastly to run the celery worker run "python -m celery -A medexer worker -E" in a separate command line (PS you will need redis install on your local machine)