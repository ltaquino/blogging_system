
# Project Title

#### Clone the repository
`git clone https://github.com/ltaquino/blogging_system`

#### Change directory to the system
`cd blogging_system`

#### To ensure environment is clear
`docker-compose down -v`

#### To build and start you container
`docker-compose up --build`

#### If error says django.db.utils.OperationalError: unable to open database file, run this command
`docker-compose exec django-web chown -R www-data:www-data /app`


#### To apply database migration , open new terminal and change directory to the project root
`docker-compose exec django-web python manage.py migrate`

#### To create super user
`docker-compose exec django-web python manage.py createsuperuser`

#### to run the test case
`docker-compose exec django-web pytest -v`

#### Test cases path
`blogging_system/blogging_system/tests/test_api.py`