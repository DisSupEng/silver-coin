from django.urls import path

from .views import DashboardView, CreateBudget

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("budget/create", CreateBudget.as_view(), name="create_budget"),
]