This project has been developed in a OSX/Linux environment so setup is written for those OS types.
As it is a test project I haven't dockerized it or written tests as to not waste time during development.

SETUP STEPS:
1. Position yourself in the unzipped folder
2. Create virtual environment 

Virtualenv package is a prerequisite for this step. After you have installed it run this command:

virtualenv -p $(which python3) env

3. Activate virtual environment 

source ./env/bin/activate 

4. Install requirements

pip install -r requirements.txt

5. Move to django root folder 

cd test_project

6. Setup django SQLite database for session management 

python manage.py migrate

7. Run the server

gunicorn config.wsgi_production --bind 0.0.0.0:8000 --workers 1