<h1 align="center"> 👋 This is Assessing project for University</h1>
<h3 align="center">A passionate full-stack developer from Uzbekistan</h3>
<h1> Intro </h1>


## First of all you have to clone this project to your own computer.
    git clone git@github.com:bobur22/Assessment_project.git
## And then open your terminal and start creating by env file
      python -m venv venv / py -m venv venv
## then activate env file.
## And after that start with installing requirements.txt
    pip install -r requirements.txt
## then make a migrations.
    python manage.py makemigrations

## and after that migrate it.
    python manage.py migrate

## before runing server create super user in order to open admin panel.
    python manage.py createsuperuser

## then finally start project.
    python manage.py runserver

#Then you can open website on your local host.
## and project is ready.
