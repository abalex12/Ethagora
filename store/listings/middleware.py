from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Skip redirect for these URLs
            excluded_paths = [
                reverse('complete_profile'),
                reverse('listings'),
                reverse('logout'),
                '/admin/',
            ]
            
            if not any(request.path.startswith(path) for path in excluded_paths):
                # Check if user needs to complete profile
                if not request.user.telegram_username or not request.user.phone:
                    return redirect('complete_profile')

        response = self.get_response(request)
        return response