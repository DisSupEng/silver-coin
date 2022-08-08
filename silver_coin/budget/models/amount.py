from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

class AmountManager(models.Manager):
    def create_amount(self, amount, parent):
        """
        This method will be called when creating a new BudgetPeriod.
        The Amount objects on the Budget must be copied so they are recorded as they were at the time 
        (remember Budget objects can change and historical data should remain unchanged).

        The name, amount_type and amount will be copied and the parent will be assigned to either the
        budget or budget_period depending on the type of the parent.
        """
        if parent.__class__ == Budget:
            # Link it to a Budget
            self.create(
                name=amount.name, 
                amount_type=amount.amount_type, 
                amount=amount.amount,
                budget=parent
            )
        elif parent.__class__ == BudgetPeriod:
            # Link it to a Budget Period
            self.create(
                name=amount.name, 
                amount_type=amount.amount_type, 
                amount=amount.amount,
                budget_period=parent
            )
        else:
            # Parent is not a Budget or BudgetPeriod, raise an error
            raise ValidationError("Amount cannot be linked to class: " + parent.__class__)

class Amount(models.Model):
    """
    An Amount represents an estimate expense/income or an actual expense/income.
    An Amount may be linked to either a Budget or BudgetPeriod but not both.
    If linked to a Budget then it is an estimate.
    If linked to a BudgetPeriod then it is an actual.
    """
    AMOUNT_TYPES = [
        ("IN", "Income"),
        ("EX", "Expenses"),
    ]

    amount_id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, blank=False, max_length=2, verbose_name="Name")
    amount_type = models.CharField(choices=AMOUNT_TYPES, null=False, blank=False, max_length=2, verbose_name="Type")
    # The maximum number of digits including decimal places is 7
    amount = models.DecimalField(null=False, blank=False, max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01, "Amount must be positive, mark as Expense if outgoing cost")])
    budget = models.ForeignKey("Budget", null=True, blank=True, default=None, db_column="budget", on_delete=models.CASCADE, verbose_name="Budget")
    budget_period = models.ForeignKey("BudgetPeriod", null=True, blank=True, default=None, db_column="budget_period", on_delete=models.CASCADE, verbose_name="Budget Period")
    # An Amount should be linked to the User
    owner = models.ForeignKey(User, null=False, blank=True, editable=False, db_column="owner", on_delete=models.CASCADE)

    # Define the model manager
    objects = AmountManager()


    def clean(self):
        """
        An Amount must be linked to either a Budget or Budget Period but not both.
        """
        if self.budget is None and self.budget_period is None:
            raise ValidationError("An Amount cannot be linked to both a Budget and BudgetPeriod")
        elif self.budget is not None and self.budget_period is not None:
            raise ValidationError("An Amount must be linked to either a Budget or BudgetPeriod")
        
        return self.clean()