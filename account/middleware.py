from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from project.models import UserProfile

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'user_id' in request.session:
            try:
                request.user = User.objects.get(pk=request.session['user_id'])
            except User.DoesNotExist:
                request.user = None

        if not request.user.is_authenticated and request.path not in [reverse('account:login'), reverse('account:register')]:
            return HttpResponseRedirect(reverse('account:login'))
        
       
        if request.user.is_authenticated and not request.user.is_superuser and request.path.startswith('/admin_panel/'):
            return HttpResponseRedirect(reverse('account:login'))  
        
        response = self.get_response(request)
        return response