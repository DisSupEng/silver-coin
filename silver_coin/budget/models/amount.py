from django.db import models
from django.core.exceptions import ValidationError

class AmountManager(models.Manager):
    def create_amount(self, amount, period, is_actual=False):
        """ 
        This method will be called when creating a new BudgetPeriod.
        The Amount objects on the Budget must be copied so they are recorded as they were at the time 
        (remember Budget objects can change and historical data should remain unchanged).

        The name, amount_type and amount will be copied and the parent will be assigned to either the
        budget or budget_period depending on the type of the parent.
        """
        # Link it to a Budget Period
        self.create(
            name=amount.name, 
            amount_type=amount.amount_type, 
            is_actual=is_actual,
            amount=0 if is_actual else amount.amount,
            budget_period=period,
        )

class Amount(models.Model):
    """
    An Amount represents an estimate expense/income or an actual expense/income.
    An Amount may be linked to either a Budget or BudgetPeriod but not both.
    If linked to a Budget then it is an estimate.
    If linked to a BudgetPeriod then it is an estimate or actual
    """
    AMOUNT_TYPES = [
        ("IN", "Income"),
        ("EX", "Expenses"),
    ]

    amount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Name")
    amount_type = models.CharField(choices=AMOUNT_TYPES, null=False, blank=False, max_length=2, verbose_name="Type")
    # Is the amount model an actual amount (i.e the actual amount that has been spent)
    # We need this because a budget period copies the amounts from the current budget and creates a record for itself
    is_actual = models.BooleanField(null=False, editable=False, default=False)
    # Is the amount a one time cost
    is_one_time_cost = models.BooleanField(null=False, default=True)
    # The maximum number of digits including decimal places is 7
    amount = models.DecimalField(null=False, blank=False, max_digits=7, decimal_places=2)
    budget = models.ForeignKey("Budget", null=True, blank=True, default=None, db_column="budget", on_delete=models.CASCADE, verbose_name="Budget", related_name="amounts")
    budget_period = models.ForeignKey("BudgetPeriod", null=True, blank=True, default=None, db_column="budget_period", on_delete=models.CASCADE, verbose_name="Budget Period")

    # Define the model manager
    objects = AmountManager()


    def clean(self):
        """
        An Amount must be linked to either a Budget or Budget Period but not both.
        Amount must be greater than zero
        One time amounts can only be linked to a Budget Period
        """
        if self.budget is None and self.budget_period is None:
            raise ValidationError("An Amount must be linked to either a Budget or BudgetPeriod")
        elif self.budget is not None and self.budget_period is not None:
            raise ValidationError("An Amount cannot be linked to both a Budget and BudgetPeriod")

        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero, mark as expense if outgoing cost")
        if self.is_one_time_cost and self.budget is not None:
            raise ValidationError("A one time amount must be linked to a Budget Period")