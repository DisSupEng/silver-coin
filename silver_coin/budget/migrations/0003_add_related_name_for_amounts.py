# Generated by Django 3.2 on 2023-09-10 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_create_actual_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amount',
            name='budget_period',
            field=models.ForeignKey(blank=True, db_column='budget_period', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='estimates', to='budget.budgetperiod', verbose_name='Budget Period'),
        ),
    ]
