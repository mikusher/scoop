#!/bin/sh
# This script automates the install last postgres database on ubuntu.
#
# force user to run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root"
    exit 1
fi


# the username of the postgres user is passed as an argument if not set the default value is "postgres"
if [ -z "$1" ]; then
    USERNAME="postgres"
else
    USERNAME="$1"
fi

# the password of the postgres user is passed as an argument if not set the default value is "postgres"
if [ -z "$2" ]; then
    PASSWORD="postgres"
else
    PASSWORD="$2"
fi

# update the package list and upgrade all packages
echo "Updating package list and upgrading all packages..."
apt-get update
apt-get upgrade -y
echo "Done."

# install postgresql version 12.0 and create the postgres user with the password passed as an argument if not set the default value is "postgres"
echo "Installing postgresql version 12.0 and creating the postgres user with the password passed as an argument if not set the default value is 'postgres'..."
apt-get install postgresql-12.0 postgresql-contrib-12.0 -y
sudo -u postgres psql -c "CREATE USER $USERNAME WITH PASSWORD '$PASSWORD';"
echo "Done."

# escalate privileges to user to admin
echo "Escalating privileges to user to admin..."
sudo -u postgres psql -c "ALTER USER $USERNAME WITH SUPERUSER;"
echo "Done."

# question if user want to alter the postgresql.conf file and set the parameters
echo "Do you want to alter the postgresql.conf file and set the parameters?"
echo "1. Yes"
echo "2. No"
read -p "Enter your choice [1-2]: " choice
# check if user input is valid
if [ $choice -lt 1 ] || [ $choice -gt 2 ]; then
    echo "Invalid choice, aborting."
    exit 1
fi
# if user choose to alter the postgresql.conf file and set the parameters
if [ $choice -eq 1 ]; then
    # open the postgresql.conf file in the editor
    nano /etc/postgresql/12.0/main/postgresql.conf
    # set the parameters
    echo "Setting the parameters..."
    sudo -u postgres sed -i 's/^#listen_addresses =.*/listen_addresses = '\'\'localhost\'\''/g' /etc/postgresql/12/main/postgresql.conf
fi
# if user choose to alter the postgresql.conf file and set the parameters
if [ $choice -eq 2 ]; then
    # set the parameters
    echo "Nothing to do."
fi
echo "Done."

# restart the postgresql service
sudo service postgresql restart

# question if user want to alter the postgresql.conf file and set the parameters
echo "Do you want to alter the postgresql.conf file and set the parameters?"
echo "1. Yes"
echo "2. No"
read -p "Enter your choice [1-2]: " choice
# check if user input is valid
if [ $choice -lt 1 ] || [ $choice -gt 2 ]; then
    echo "Invalid choice, aborting."
    exit 1
fi
# if user choose to alter the pg_hba.conf file and set the parameters
if [ $choice -eq 1 ]; then
    # set the parameters
    echo "Setting the parameters..."
    sudo -u postgres sed -i 's/^#host.*/host all all all trust/g' /etc/postgresql/12/main/pg_hba.conf
fi
# if user choose to alter the postgresql.conf file and set the parameters
if [ $choice -eq 2 ]; then
    # set the parameters
    echo "Nothing to do."
fi
echo "Done."
#
# restart the postgresql service
sudo service postgresql restart
# all done
echo "All done."