from django.urls import path

from .views import DashboardView
from .views import CreateBudget
from .views import EditBudget
from .views import DeleteBudget
from .views import AmountList
from .views import CreateIncome
from .views import EditIncome
from .views import DeleteIncome

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # Budget URLs
    path("budget/create", CreateBudget.as_view(), name="create_budget"),
    path("budget/edit", EditBudget.as_view(), name="edit_budget"),
    path("budget/delete", DeleteBudget.as_view(), name="delete_budget"),
    # Amount URLs
    path("amount/", AmountList.as_view(), name="amount"),
    path("amount/create", CreateIncome.as_view(), name="create_amount"),
    path("amount/edit/<int:pk>", EditIncome.as_view(), name="edit_amount"),
    path("amount/delete/<int:pk>", DeleteIncome.as_view(), name="delete_amount")
]