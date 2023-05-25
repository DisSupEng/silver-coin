# Generated by Django 3.2 on 2023-05-25 08:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('budget_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25, validators=[django.core.validators.MaxLengthValidator(25, 'Name cannot be greater than 25 characters')], verbose_name='Name')),
                ('description', models.CharField(blank=True, default='', max_length=250, validators=[django.core.validators.MaxLengthValidator(250, 'Description cannot be greater than 250 characters')], verbose_name='Description')),
                ('period_type', models.CharField(choices=[('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], default='weeks', max_length=6, verbose_name='Period Type')),
                ('period_length', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Period Length must be greater than zero')], verbose_name='Period Length')),
                ('owner', models.ForeignKey(db_column='owner', editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetPeriod',
            fields=[
                ('budget_period_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField(default=django.utils.timezone.now, verbose_name='Start Date')),
                ('end_date', models.DateField(editable=False, verbose_name='End Date')),
                ('budget', models.ForeignKey(db_column='budget', on_delete=django.db.models.deletion.CASCADE, to='budget.budget', verbose_name='Budget')),
            ],
        ),
        migrations.CreateModel(
            name='Amount',
            fields=[
                ('amount_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('amount_type', models.CharField(choices=[('IN', 'Income'), ('EX', 'Expenses')], max_length=2, verbose_name='Type')),
                ('is_actual', models.BooleanField(default=False, editable=False)),
                ('is_one_time_cost', models.BooleanField(default=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7)),
                ('budget', models.ForeignKey(blank=True, db_column='budget', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amounts', to='budget.budget', verbose_name='Budget')),
                ('budget_period', models.ForeignKey(blank=True, db_column='budget_period', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='budget.budgetperiod', verbose_name='Budget Period')),
            ],
        ),
    ]
