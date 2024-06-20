# myapp/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_paths = [
            reverse('login'),
            reverse('signup'),
            reverse('admin:index'),  # Add any other allowed paths here
        ]

        if not request.user.is_authenticated and request.path not in allowed_paths:
            return redirect('login')

        response = self.get_response(request)
        return response
