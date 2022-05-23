from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView

from trains.forms import TrainForm
from trains.models import Train


# Create your views here.
class TrainsList(ListView):
    model = Train
    template_name = 'trains/trains_list.html'
    paginate_by = 5


class TrainInfo(DetailView):
    model = Train
    template_name = 'trains/train_info.html'


class TrainCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/create_train.html'
    success_message = "Поезд был успешно добавлен"


class TrainUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update_train.html'
    success_url = reverse_lazy('cities:cities_list')
    success_message = "Поезд был успешно отредактирован"


class TrainDelete(LoginRequiredMixin, DeleteView):
    model = Train
    success_url = reverse_lazy('route:routes_list')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удален')
        return self.delete(request, *args, **kwargs)
