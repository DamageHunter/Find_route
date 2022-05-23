from django.urls import path

from route.views import FindRoute, SaveRoute, RoutesList, RouteInfo, RouteDelete

app_name = 'route'

urlpatterns = [
    path('', FindRoute.as_view(), name='home'),
    path('save_route/', SaveRoute.as_view(), name='save_route'),
    path('routes/', RoutesList.as_view(), name='routes_list'),
    path('route_detail/<int:pk>/', RouteInfo.as_view(), name='route_info'),
    path('route_delete/<int:pk>/', RouteDelete.as_view(), name='route_delete'),
]
