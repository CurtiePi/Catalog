# Catalog project
This project is located on a remote server.


### Connecting to the Server
*Server IP*: 52.39.197.108

*SSH command*: ssh grader@52.39.197.108 -p 2200

Application can be accessed in a browser via the folloing url:

*Web URL*: http://ec2-52-39-197-108.us-west-2.compute.amazonaws.com/

### SOFTWARE INSTALLED
*finger*
configuration changes: NONE

*apache2*
configuration changes:

* *Change the server name*:
ServerName "52.39.197.108"

* *Root should not give 'permission denied' message*
```
<Directory />
    Options Indexes FollowSymLinks Includes ExecCGI
    AllowOverride All
    Order deny,allow
    Allow from all
</Directory>
```
     
* *Define wsgi script directory*
```
<Directory /usr/local/www/wsgi-scripts/catalog>
        Order allow,deny
        Allow from all
</Directory>
```
* *Updated .htaccess to disallow access to .git*
RedirectMatch 404 /\.git

* *Create application configuration file: /etc/apache2/sites-available/catalog.conf*

Application specific error logs:
```
	ErrorLog ${APACHE_LOG_DIR}/catalog_error.log
	CustomLog ${APACHE_LOG_DIR}/catalog_access.log combined
```

Define script location also define path of python modules:
```
        WSGIScriptAlias / /usr/local/www/wsgi-scripts/catalog/catalog.wsgi
        WSGIDaemonProcess 52.39.197.108 python-path=/usr/local/lib/python2.7/dist-packages:/usr/local/lib/python2.7/site-packages:/usr/local/www/wsgi-scripts/catalog
        WSGIProcessGroup 52.39.197.108
```

*libapache2-mod-wsgi*
Configuration changes:

Create a wsgi file called *catalog.wsgi* and import the app in project.py as application

*python-psycopg2*
Configuration changes: NONE

*git*
Configuration changes:
modified .gitignore to include .pyc files

*python-flask*
Configuration changes: NONE

*python-sqlalchemy*
Configuration changes: NONE

*python-flask-sqlalchemy*
Configuration changes: NONE

*python-werkzeug*
Configuration changes: NONE

*python-oauth2client*
Configuration changes: NONE

*postgresql-9.3*
Configuration changes: NONE

*python-loggingx*
Configuration changes: NONE



### About this project:

####The structure of this project is as follows
<pre>
catalog
|
- database_setup.py
- client_secrets.json
- createsportinggoods.py
- fb_client_secrets.json
- project.py
|
--|
  - static
  |      |
  |      - styles.css
  |      |
  |      |
  |      - images
  |             |
  |             - default
  |             |
  |             - NoPicAvailable.png
  |
  |
  - templates
         |
         - categories.html
         - deleteequipment.html
         - editequipment.html
         - equipment.html
         - equipmentdetail.html
         - header.html
         - latestequipment.html
         - login.html
         - newequipment.html
</pre>

####The database has 3 tables:

User
- id      integer
- name    string
- picture string
- email   string

Category
- id      integer
- name    string

Equipment
- id      integer
- name    string
- price   string
- image   string
- description string
- entry_time  datetime
- catergory_id integer foreign key Category.id

####Database is created and populated by running this python script

$ python createsportinggoods.py


####How it works (hopefully):

The main screen should have two parts:
1. Categories
2. Equipment listing

The first listing is equipment recently added to the database, currently set at anyting 
added less than 16 hours from the current time.

Clicking on a category will list all the euipment in that category, 

Clicking on the equipmnt will take you to a detailed description page.

None of the above screens allows the user to edit, or add information. In order
to edit, delete or create new equipment entries the user must log in.

Logging in utilizes both facebook and google authentication.

Once a user is authenticated via google or facebook the my create equipment from the 
Category Equipment listing page - equipment.html

The user may delete or edit equipment from:
Equipment Detail page - equipmentdetail.html
Category Equipment listing page - equipment.html

When they user logs in the session is populated with user information which can be used
later. When the user disconnects, the session data is cleared.

Note when a user edits, adds equipment if no image is assigned the equipment will be given
a default image. Also the application will create category specific directories to hold the 
images for equipment in that category. Uploading a new image will remove the old image and 
deleting the equipment will remove its related image unless it's a default image.


Some private notes:
1. Originally this project used sqlite for the database, changing to postgresql became a challenge the main one being
that sqlalchemy's create_engine for sqllite uses the following syntax for the url parameter:

<pre>
'sqlite:///dbname'
</pre>

whereas for postgressql the syntax is:

<pre>
'postgresql://user:password@server:port/dbname'
</pre>

Why was this an issue? Because the follwing syntax will also work:

<pre>
'postgresql:///dbname'
</pre>

and I (like an idiot) tried using this syntax:
<pre>
'postgresql:///user:password@server:port/dbname'
</pre>

which only throws an OperationalException database user:password@server:port/dbname does not exist.

2. Another issue was getting the server to recognize the modules, which led to the aforemention configuration changes in 
/etc/apache2/sites-available/catalog.conf file.
