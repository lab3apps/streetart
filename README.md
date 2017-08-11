# Christchurch street art

Written by Lab3 Limited for Watch this Space

### Installation
Install python 3
Update pip3
Install postgreSQL (I reccomend postgres.app for OSX)
Install virtualenv

Set up a virtual environment.

`virtualenv -p python3 env`
or
`virtualenv --python=[path to python 3] env`
and activate it:

`source env/bin/activate`

To deactivate, in the same directory simply run `deactivate`.

Then install the supporting scripts:

`pip3 install -r requirements.txt`

Create a user `***REMOVED***`:

	- On Mac: Open `System Preferences` then `Users & Groups` and create a user through the interface.

	- On Linux: As root, run `useradd ***REMOVED***` then `passwd ***REMOVED***` choosing a suitable password.


### Use

Run the server locally
`python3 manage.py runserver`
Or to customise ip and port (default is http://127.0.0.1:8000/)
`python3 manage.py runserver ip:port`

### Changing the Model

Change your models (in models.py).
Run `python3 manage.py makemigrations` to create migrations for those changes
Run `python3 manage.py migrate` to apply those changes to the database.