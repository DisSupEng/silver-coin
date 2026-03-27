# Silver Coin
A budgeting app built in Django.

## What is this application?
Silver Coin is a budgeting app built to track expected incomes and expenses against actual incomes and expenses.

The core component of this application is the `Budget` model. It's main purpose is to define how often you want
your budget to occur, a specific number of days, weeks, months or years.

A `Budget` will have `Amounts` associated with it. `Amounts` are estimates of your incomes and expenses.
As an example you may expect to get $1,200 from work and spend $100 on food, $50 on power and $150 on rent per week.

`Budget Periods` are periods of time where you specify the `Actual Amounts` that have occurred for the different
items in your budget. A `Budget Period` starts on the date you specify and end based on the length you specified
in your `Budget`. `Budget Periods` cannot overlap, when you create a `Budget Period` it will be checked against the
existing records to ensure no overlap has occurred.

The final piece of this application is `Actual Amounts`. As stated these store the actual amounts that you have
received for your incomes and expenses. It is associated with an `Amount` you have in your budget and must occur
within the timeframe of the `Budget Period` you are adding it to.

## Getting started

**Note: This application has been developed in Linux and may not work as expected on other operating systems.**

### Setting up the application

This application can currently only be run locally using Docker. Please ensure you have docker installed before continuing.
Please also ensure that you have Python installed.

Clone the repository to a directory on your machine, navigate to that directory in the terminal.

You need to create a `.env` file in the root directory of the project with the following lines (Please replace the values inside <> with your own values and remove <>).
```
DJANGO_SECRET_KEY=""
POSTGRES_DATABASE="<my_budget_database>"
POSTGRES_USER="<database_user_example>"
POSTGRES_PASSWORD="<database_password_example>"
```

Next we need to generate a secret key for Django. This can be done by installing Django in a virtual environment and generating a secret key.
```
python3 -m venv <path_of_new_venv>
. ./<path_of_new_venv>/bin/activate
pip install ./requirements.txt
python3
> from django.core.management.utils import get_random_secret_key
> get_random_secret_key()
```

Please copy and paste the value returned from the function and put it into the `DJANGO_SECRET_KEY` value above without the single quotes at the beginning and end.

```
docker compose build
docker compose up -d
```

You should now be able to see the application running in your web browser by going to `localhost:8000`. You can either create a new user for yourself or see the `Quick Start` section below if you just want to see the application running with some dummy data.

To stop the application run
```
docker compose down
```

## Quick Start

