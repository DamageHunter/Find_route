from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegistrationFrom


# Create your views here.
class UserLogin(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = 'routes/find_route.html'

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f'{user}! Вы успешно авторизовались')
        return super().form_valid(form)


class CreateUser(CreateView):
    model = User
    form_class = UserRegistrationFrom
    template_name = 'users/registration.html'

    def get_success_url(self):
        messages.success(self.request, 'Вы успешно зарегистрировались')
        return reverse('users:user_login')
