# todo_app
A TODO app written in Django for basic task list.

# Installing Dependencies
***************************
1.Install virtual environment using:
::

    $ sudo pip install virtualenv

2.Create one virtual environment.

The following commands will create an env called ``vir`` :
::

    $ python3 -m venv vir
    
3.Now activate the ``assign_env`` environment using:
::

    $ source vir/bin/activate
    (vir)[user@host]$

Setting the project
***************************
1.Run the command in your virtual environment.
::

    $ cd /path/to/todo_app
    
2. Install the requirements using: 
::

    $ pip install -r requirements.txt

Running the code
***************************
run this command:
::

    $ python manage.py createsuperuser
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py collectstatic
    $ python manage.py runserver    
You will get something like the following on running the above code −
::

    Performing system checks...

    System check identified no issues (0 silenced).
    May 24, 2017 - 02:46:08
    Django version 1.11, using settings 'todo_app.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
Now open your browser and enter this address:    
::

   http://127.0.0.1:8000/

Updating todo data by celery
******************************
open two new terminal at the project root in your virtual environment and run this command:
::

    $ celery -A todo worker -l info 
    $ celery -A todo beat -l info 
