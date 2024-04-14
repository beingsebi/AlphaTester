from django.http import HttpResponse
from .forms import NewUserForm
from django.views.generic.edit import FormView
from django.contrib.auth.models import User

def index(request):
    return HttpResponse("Hello, world. You're at the account index.")


class SignUpView(FormView):
    """
    Display the register form.
    """
    form_class = NewUserForm
    template_name = 'account/register.html'
    success_url = '/account/login/'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)