from django.urls import path

from .views import DashboardView, BudgetCreateView

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("budget_create/", BudgetCreateView.as_view(), name="budget_create"),
]