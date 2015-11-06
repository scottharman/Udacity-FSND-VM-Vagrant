apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
sudo apt-get -qqy install python-dev libmysqlclient-dev
pip install bleach
pip install oauth2client
pip install requests
pip install httplib2
sudo pip install wtforms wtforms-alchemy --upgrade
sudo pip install --upgrade mysql-python flask-login==0.2.9 flask-sqlalchemy
 sudo pip install flask-whooshalchemy
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'createdb'
su vagrant -c 'createdb forum'
#su vagrant -c 'createdb tournament'
su vagrant -c 'createdb catalog'
#su vagrant -c 'psql -f /vagrant/tournament/tournament.sql'
su vagrant -c 'psql forum -f /vagrant/forum/forum.sql'
sudo sed -i "/listen_addresses/c\listen_addresses = '*'" /etc/postgresql/9.3/main/postgresql.conf
sudo sed -i '1,/^host/s/^host/host\t\tall\t\tall\t\t0.0.0.0\/0\t\ttrust\n#host/' /etc/postgresql/9.3/main/pg_hba.conf
sudo /etc/init.d/postgresql reload

vagrantTip="[35m[1mThe shared directory is located at /vagrant\nTo access your shared files: cd /vagrant(B[m"
echo -e $vagrantTip > /etc/motd
