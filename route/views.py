from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, CreateView, ListView, DetailView, DeleteView

from route.models import Route
from services.calculate_routes import find_routes
from route.forms import FindRouteForm, SaveRouteForm
from trains.models import Train


class FindRoute(FormView):
    template_name = 'routes/find_route.html'
    form_class = FindRouteForm
    success_url = 'routes/find_route.html'

    def form_valid(self, form):
        try:
            routes_data = find_routes(form.cleaned_data)
        except ValueError as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(reverse('route:home'))

        return render(request=self.request, template_name=self.template_name,
                      context={'form': self.form_class, 'routes': routes_data})


class SaveRoute(LoginRequiredMixin, CreateView):
    model = Route
    form_class = SaveRouteForm
    success_url = '/'
    template_name = 'routes/save_route.html'

    def get_initial(self):
        data = self.request.GET
        initial = super().get_initial()

        initial['from_city'] = int(data['from_city'])
        initial['to_city'] = int(data['to_city'])
        initial['travel_time'] = data['travel_time']
        trains = [int(train) for train in data['trains'].split(',') if train.isdigit()]
        initial['trains'] = Train.objects.filter(id__in=trains)
        return initial


class RoutesList(ListView):
    model = Route
    template_name = 'routes/routes_list.html'
    paginate_by = 5


class RouteInfo(DetailView):
    model = Route
    template_name = 'routes/route_info.html'


class RouteDelete(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('route:routes_list')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален')
        return self.delete(request, *args, **kwargs)
