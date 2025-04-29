from .apps import MapConfig
from django.urls import path
from .views import (RouteListView, RouteUpdateView, RouteDeleteView, RouteDetailView,
                    KaliningradRouteView, RouteSaveView)

app_name = MapConfig.name

urlpatterns = [
    path('route/list/', RouteListView.as_view(), name='route_list'),
    # path('route/create/', RouteCreateView.as_view(), name='route_create'),
    path('route/<int:pk>/', RouteDetailView.as_view(), name='route_retrieve'),
    path('route/update/<int:pk>', RouteUpdateView.as_view(), name='route_update'),
    path('route/delete/<int:pk>', RouteDeleteView.as_view(), name='route_destroy'),
    # path('api/nearby/', NearbyPOIAPIView.as_view(), name='nearby_poi'),
    path('', KaliningradRouteView.as_view(), name='kaliningrad_route'),
    path('api/save_route/', RouteSaveView.as_view(), name='save_route'),
]
