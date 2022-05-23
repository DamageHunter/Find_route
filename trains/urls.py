from django.urls import path

from trains.views import TrainsList, TrainInfo, TrainCreate, TrainUpdate, TrainDelete

app_name = 'trains'

urlpatterns = [
    path('', TrainsList.as_view(), name='trains-list'),
    path('detail/<int:pk>/', TrainInfo.as_view(), name='train-info'),
    path('create/', TrainCreate.as_view(), name='create-train'),
    path('update/<int:pk>/', TrainUpdate.as_view(), name='update-train'),
    path('delete/<int:pk>/', TrainDelete.as_view(), name='delete-train')
]
