# GroupUp

## Installation for development

Use of [venv](https://docs.python.org/3/tutorial/venv.html) is recommended.

Change to the root directory of the project and run

```shell
python3 -m venv venv
```

to create a virtual environment with name "venv".
Then source the environment.
For Windows:

```shell
venv/Scripts/activate.bat
```

For MacOS/Linux:

```bash
source venv/bin/activate
```

Then install all the required packages with

```shell
python3 -m pip install -r requirements.txt
```

The project is configured to use SQLite3 as the database, but this can easily
be configured to another database, such as PostgreSQL or MySQL, see the django [documentation](https://docs.djangoproject.com/en/4.0/ref/databases/).
After installing the required packages, you need to migrate the database tables to
database. First change the directory to the one containing the manage.py file. Then
run:

For Windows:

```shell
py manage.py migrate
```

For MacOS/Linux:

```bash
python3 manage.py migrate
```

You can now run the server:

For Windows:

```shell
py manage.py runserver
```

For MacOS/Linux:

```bash
python3 manage.py runserver
```

## Production

For production, you should look at using a better webserver than Django's inbuilt,
see for example Apache Web Server. For a complte guide see this [documentation](https://docs.djangoproject.com/en/4.0/howto/deployment/).

## Tests

There are a few tests for the application, but these are constrained to the models.
To see the result of the tests, run:

For Windows:

```shell
py manage.py test
```

For MacOS/Linux:

```bash
python3 manage.py test
```

## Static and uploaded files

Static files are stored in its own static folder. Uploaded files are not in git, but is configured to be saved
in a folder named "uploads", which lies in the same directory as manage.py. The structure is uploads/{groups, users}.
The filename for users should be {username}.{png|jpg|gif}, since username is unique. The group photos takes it name
from the group name, and its primary key. However, due to a bug, the first picture for a group will have the name 
{groupname}_None.jpg, since at the time of creation, the group does not "exist" in the database, and therefore has no
primary key.
