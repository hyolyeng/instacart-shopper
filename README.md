# instacart-shopper


# Shopper Challenge Details: 
https://app.greenhouse.io/tests/95a7fc0ee75ebdcb95594c8e526fa478

# Sample app running at:
https://peaceful-shelf-75383.herokuapp.com/

# Technologies
Django
Python
SQLite

# Running the Application

To run the application locally, clone this repository and run the following commands from the project directory.

Apply db migrations:

python manage.py migrate

Run django server:

python manage.py runserver

This will start the django server on port 8000. The landing page can be accessed at:

http://localhost:8000/

# Shopper Registration

https://peaceful-shelf-75383.herokuapp.com/

A simple webpage to allow shoppers to enter basic information to be entered into the hiring funnel. If the entered email is already in the hiring funnel, then the user is taken to the application status page, where it simply shows the application status. (one of applied, quiz_started, quiz_completed, onboarding_requested, onboarding_completed, hired, rejected)

Otherwise, the user is taken to the next page to fill in their name, phone number and zip code. Each input is validated before the user is able to submit. (Name cannot be empty, phone number should be digits of length 9-15, zip should be 5 digits.) After the user finishes that step, they're taken to the background check permission page, and only after the user finally clicks on I Give Permission does the data get written to the database.

# Funnel

http://https://peaceful-shelf-75383.herokuapp.com/shoppers/funnel?start_date=START_DATE&end_date=END_DATE

where START_DATE and END_DATE are of format YYYY-MM-DD

Returns a JSON string with weekly hiring funnel data, or an empty JSON if given dates are not valid.