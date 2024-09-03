from django.contrib.auth.views import LoginView,LogoutView
from .forms import CustomAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return self.request.GET.get('next', '/')
    
class CustomLogoutView(LogoutView):
    template_name = 'logged_out.html'    
