# check-driver

This repo includes:
* Django service with DRF which serves to create checks and render PDF.
* Simple imitation of printer, which sends request to receive PDF for printing them.

1. This app creates a check with status 'new' when receive new order request.
2. The next step celery worker renders PDF invoice from HTML and changes status to 'rendering'.
3. After that Printer sends request with its api_key to receive list of new unprinted checks for itself.
4. After that Printer sends another request to download PDF and prints them.
5. After all Printer sends request to change status of check to 'printed'.

To run this project you need:
1. Create a virtual environment
2. Run `python -m pip install -r requirements.txt`
3. Run `docker-compose up`
4. Run migration `python manage.py migrate`
5. Run django server `python manage.py runserver`
6. Run celery `celery -A checkdriver worker --loglevel=INFO`

***Note***: Also, you may want to populate db, you can do that by running `python manage.py loaddata data.json`