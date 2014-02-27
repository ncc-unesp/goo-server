README
======

REQUIREMENTS
============

   $ sudo pip install -r requirements.txt

COVERAGE
========

python-coverage run --source='.' manage.py test core dispatcher storage
python-coverage html -d docs/coverage --omit='*/migrations/*,*/__init__.py,manage.py'

DOCUMENTATION
=============

cd docs ;  make clean ; make html ; firefox ../portal/static/index.html ; cd -

MAP
===

rm world.json ; ogr2ogr -overwrite -select name -f "GeoJSON" -simplify 0.8 world.json ne_50m_admin_0_countries.shp; du -sck world.json ; du -scm world.json

DEPLOYMENT
==========

For local deployment (using apache as proxy)
--------------------------------------------

# a2enmod proxy proxy_http

# (config file)
ProxyPass /api http://submit.grid.unesp.br:8000/api

<Directory /<path>/goo-server/portal/>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride None
        Order allow,deny
        allow from all
</Directory>
Alias /portal /<path>/goo-server/portal

Enable cronjob (watchdog)
-------------------------

Add to crontab:

  PYTHONPATH=/var/lib/goo/goo-server:$PYTHONPATH DJANGO_SETTINGS_MODULE=gooserver.settings.production /var/lib/goo/goo-server/dispatcher/tools/watchdog.py
