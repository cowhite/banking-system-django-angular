Banking System using Django and Angular Js:
==============================================

[![Build Status](https://travis-ci.org/cowhite/banking-system-django-angular.svg?branch=master)](https://travis-ci.org/cowhite/banking-system-django-angular)
[![Coverage Status](https://coveralls.io/repos/github/cowhite/banking-system-django-angular/badge.svg?branch=master)](https://coveralls.io/github/cowhite/banking-system-django-angular?branch=master)

Issues - https://github.com/cowhite/banking-system-django-angular/issues

Installation and Usage:
-----------------------
git clone git@github.com:cowhite/banking-system-django-angular.git
cd banking-system-django-angular/project_template
mkvirtualenv banking-system
pip install -r requirements.txt
python manage.py migrate
cd staticfiles/angular-src
npm install
bower install
grunt minify

cd ../../
python manage.py runserver

Running celery for background tasks:
Install Rabbitmq or redis.
In another terminal, activate environment(workon banking-system) and run below command:

    celery -A project_template worker -l info


Contributing by outside members:
-------------------------------
You can start contributing after we complete the basic features. For now, please dont send any PRs.
