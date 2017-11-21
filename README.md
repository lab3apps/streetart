# Christchurch Street Art

Written by Lab3 Limited for Watch This Space

### Pre-Requisites

[Python 3](https://www.python.org/downloads/) (you'll need to [upgrade `pip`](https://pip.pypa.io/en/stable/installing/#upgrading-pip))

[VirtualEnv](https://virtualenv.pypa.io/en/stable/installation/)

Memcached

  - OSX `brew install memcached`

  - Debian/Ubuntu `sudo apt-get install memcached`

----

### Installation

It is strongly recommended that you use a Virtual Environment to manage dependencies:


`virtualenv -p python3 env`

or

`virtualenv --python=[path to python 3] env`

and activate it:

`source env/bin/activate`

To deactivate, in the same directory simply run `deactivate`.

Then install the supporting scripts:

`pip3 install -r requirements.txt`

----

### Development

#### Setting up a development environment

Follow the instructions [here](https://docs.djangoproject.com/en/1.11/ref/contrib/gis/install/) to install the required GIS libraries.

If you run into a `GEOSException` error then [this](https://stackoverflow.com/questions/18643998/geodjango-geosexception-error) may be helpful.

----

### Deployment

#### Setting up a production environment

Follow [this](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04) guide, except clone this project rather than creating a new Django project.

Install PostGIS on the server as per [this](http://www.gis-blog.com/how-to-install-postgis-2-3-on-ubuntu-16-04-lts/) guide.

Install geospatial libraries for GeoDjango
`sudo apt-get install binutils libproj-dev gdal-bin`

#### Running locally

Copy `settings_secret.py.template` and rename to `settings_secret.py`.

##### Setting up a database connection

Tunnel to the server you set up in the previous step for database access
`ssh -N -L 5432:localhost:5432 USER@REMOTE_URL`

This is structured as `ssh -N -L LOCAL_PORT:LOCAL_ADDRESS:REMOTE_PORT USER@REMOTE_URL`

Change `LOCAL_PORT` to any free port but make sure to change the `PORT` in the `DATABASES` section of `settings_secret.py` to match the port you choose.

Run the server locally
`python3 manage.py runserver`
Or to customise ip and port (default is http://127.0.0.1:8000/)
`python3 manage.py runserver IP:PORT`


#### Update Server Deployment

Run these commands on the production server:

`cd ~WTSAdmin/watch_this_space/streetart`

`source env/bin/activate`

`git pull`

`python manage.py migrate`

`python manage.py collectstatic`

`deactivate`

`sudo systemctl restart gunicorn` (or via restart.sh script)

### Changing the Model

Change your models (in models.py).

Run `python3 manage.py makemigrations` to create migrations for those changes (if using ssh tunnelling then only run this on the server to avoid mismatched Models and Database structure).

Run `python3 manage.py migrate` to apply those changes to the database.

