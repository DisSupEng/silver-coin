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
