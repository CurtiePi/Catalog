import sys
import logging, logging.handlers
logging.basicConfig(filename='/var/log/python2.7/catalog.log',
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

sys.path.append('/usr/local/www/wsgi-scripts/catalog')

logging.info('Importing the app as application')

from project import app as application
