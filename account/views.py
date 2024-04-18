from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from .forms import NewUserForm


def index(request):
    return HttpResponse("Hello, world. You're at the account index.")


class SignUpView(CreateView):
    model = User
    form_class = NewUserForm
    template_name = 'account/register.html'
    success_url = '/account/login/'
