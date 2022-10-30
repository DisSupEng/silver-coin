from django.urls import path

from .views import DashboardView, BudgetWizard

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("budget_wizard/", BudgetWizard.as_view(), name="budget_wizard"),
]