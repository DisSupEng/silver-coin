from django.urls import path

from .views import DashboardView
from .views import CreateBudget
from .views import EditBudget
from .views import DeleteBudget

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("budget/create", CreateBudget.as_view(), name="create_budget"),
    path("budget/edit", EditBudget.as_view(), name="edit_budget"),
    path("budget/delete", DeleteBudget.as_view(), name="delete_budget"),
]