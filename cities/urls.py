from django.urls import path

from cities.views import CitiesView, CityInfo, CityCreate, CityUpdate, CityDelete

app_name = 'cities'

urlpatterns = [
    path('', CitiesView.as_view(), name='cities-list'),
    path('detail/<int:pk>', CityInfo.as_view(), name='city'),
    path('create/', CityCreate.as_view(), name='create-city'),
    path('update/<int:pk>', CityUpdate.as_view(), name='update-city'),
    path('delete/<int:pk>', CityDelete.as_view(), name='delete-city')
]
