# Readme file for Udacity Catalog application
cd to `/vagrant/catalog`

run  `.application.py`

The database should have been set up in the pg_config.sh shell script, but if not, you should be able to create the necessary by running

`psql -f /vagrant/catalog/catalog.sql`

## Application brief:
The functionality implemented allows basic CRUD operations for products, and doesn't yet implement support for external images, but this will be worked on. Categories are currently hardwired, and code will be added to create new categories but not edit them. Removed the standalone user classes but these will be re-added, as well as stright user authentication. Currently you can login with google plus, but haven't added support for facebook login.  

### Issues and comments:
Had difficulty with understanding the json constructs, and ultimately found the solution on stackoverflow ([http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask](http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask)) It still doesn't render quite the way I'd like, and can't work out why. Unfortunately I am travelling again this week, so will do a final commit when time permits and will have to live with the issues.
