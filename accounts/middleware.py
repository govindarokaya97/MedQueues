from django.shortcuts import redirect
from django.urls import reverse

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.user.is_authenticated
            and request.user.force_password_change
            and request.path not in (
                reverse("force_password_change"),
                reverse("logout"),
            )
        ):
            return redirect("force_password_change")

        return self.get_response(request)