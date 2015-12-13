Provisioning a new site
=======================

## required packages:

* nginx
* Python 3
* Git
* pip
* virtualenv

e.g.,, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## Nginx Virtual Host config

* see nginx.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Upstart Job

* see gunicorn-upstart.template.conf
* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:
Assumer we have a user account at /home/username

/home/username
|___ sites
     |___ SITENAME
          |___ database
          |___ source
          |___ static
          |___ virtualenv
