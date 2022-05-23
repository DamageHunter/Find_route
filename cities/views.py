from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.views.generic.edit import DeleteView

from cities.forms import CityForm
from cities.models import City


class CitiesView(ListView):
    model = City
    template_name = 'cities/cities_list.html'
    paginate_by = 5


class CityInfo(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/city_info.html'


class CityCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = City
    template_name = 'cities/create_city.html'
    form_class = CityForm
    success_message = "Город был успешно добавлен"


class CityUpdate(LoginRequiredMixin, UpdateView):
    model = City
    fields = ['name']
    template_name = 'cities/update_city.html'
    success_url = reverse_lazy('cities:cities-list')
    login_url = reverse_lazy('users:user_login')


class CityDelete(LoginRequiredMixin, DeleteView):
    model = City
    success_url = reverse_lazy('cities:cities-list')

    def get(self, request, *args, **kwargs):
        messages.success(self.request, 'Город успешно удален')
        return self.delete(request, *args, **kwargs)
