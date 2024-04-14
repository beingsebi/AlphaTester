from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView


def index(request):
    return HttpResponse("Hello, world. You're at the account index.")

class SignUpView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'account/register.html'
    success_url = '/account/login/'