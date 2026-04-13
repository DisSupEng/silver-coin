from django.http import HttpResponseNotFound

from budget.models import Budget, Goal

class CheckGoalOwner():
    """
    A mixin that checks whether the owner of the goal is the same as the user performing the request.
    """

    """
    Adds a check at the start of the get request to check the owner.
    Also checks that the user actually has a budget of their own.0
    """
    def check_owner(self, goal_id, user) -> bool:
        """
        Checks that the user is the owner of the goal they are trying to access.

        :param: goal_id, the id of the amount object
        :param: user, the user making the request

        :returns: True if owner, 302 if they do not have a budget, 404 if they are trying to aceess an amount that is not theirs
        """
        # If the user does not have a budget redirect to dashboard
        try:
            Budget.objects.get(owner=user)
        except Budget.DoesNotExist:
            return redirect(reverse("dashboard"))
        try:
            goal = Goal.objects.get(pk=goal_id)
            if goal.budget.owner != user:
                return HttpResponseNotFound()
        except Goal.DoesNotExist:
            return HttpResponseNotFound()
        # They have a budget and they are the owner
        return True

    def get(self, request, *args, **kwargs):
        """
        Override to check the owner and redirect if required.
        """
        owner_response = self.check_owner(kwargs["pk"], request.user)

        if owner_response is not True:
            # Is a redirect or 404
            return owner_response
        # Owner OK, continue
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """
        Override to check the owner and redirect if required.
        """
        owner_response = self.check_owner(kwargs["pk"], request.user)
        if owner_response is not True:
            # Is a redirect or 404
            return owner_response
        # Owner OK, continue
        return super().post(request, *args, **kwargs)