from django.urls import path

from .views import DashboardView
from .views import CreateBudget
from .views import EditBudget
from .views import DeleteBudget
from .views import BudgetPeriodList
from .views import CreateBudgetPeriod
from .views import EditBudgetPeriod
from .views import DeleteBudgetPeriod
from .views import AmountList
from .views import CreateIncome
from .views import EditIncome
from .views import DeleteIncome
from .views import CreateExpense
from .views import EditExpense
from .views import DeleteExpense
from .views import ActualAmountList
from .views import CreateActualIncome

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # Budget URLs
    path("budget/create", CreateBudget.as_view(), name="create_budget"),
    path("budget/edit", EditBudget.as_view(), name="edit_budget"),
    path("budget/delete", DeleteBudget.as_view(), name="delete_budget"),
    # BudgetPeriod URLs
    path("budget_period/", BudgetPeriodList.as_view(), name="budget_period"),
    path("budget_period/create", CreateBudgetPeriod.as_view(), name="create_budget_period"),
    path("budget_period/edit/<int:pk>", EditBudgetPeriod.as_view(), name="edit_budget_period"),
    path("budget_period/delete/<int:pk>", DeleteBudgetPeriod.as_view(), name="delete_budget_period"),
    # Amount URLs
    path("amount/", AmountList.as_view(), name="amount"),
    path("income/create", CreateIncome.as_view(), name="create_income"),
    path("income/edit/<int:pk>", EditIncome.as_view(), name="edit_income"),
    path("income/delete/<int:pk>", DeleteIncome.as_view(), name="delete_income"),
    path("expense/create", CreateExpense.as_view(), name="create_expense"),
    path("expense/edit/<int:pk>", EditExpense.as_view(), name="edit_expense"),
    path("expense/delete/<int:pk>", DeleteExpense.as_view(), name="delete_expense"),
    # Actual Amount URLs
    path("budget_period/<int:period_id>/actual/", ActualAmountList.as_view(), name="actual_amount"),
    path("budget_period/<int:period_id>/actual/create/", CreateActualIncome.as_view(), name="create_actual_income"),
    #path("budget_period/<int:period_id>/actual/edit/<int:pk>", EditActualAmount.as_view(), name="edit_actual_amount"),
    #path("budget_period/<int:period_id>/actual/delete/<int:pk>", DeleteActualAmount.as_view(), name="delete_actual_amount")
]