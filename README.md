# pestimator 
Find Angular Front-End here <a>https://github.com/cval245/pestimator-front-user</a>

credentials: 
user: tim
pass: Belgrade2010


#  make sure to point to appropriate venv
crontab -e 
37 0-23/2 * * * python ~/pestimator/manage.py update_rates
