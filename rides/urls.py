from django.urls import path

from .views import TripView, RideViewSet, DriverViewSet

app_name = 'ride'

urlpatterns = [
    path('', TripView.as_view({'get': 'list'}), name='trip_list'),
    path('<uuid:trip_id>/', TripView.as_view({'get': 'retrieve'}), name='trip_detail'),
    path('rides/', RideViewSet.as_view({'get': 'list', 'post': 'create'}), name='ride_list'),
    path('<uuid:pk>/', RideViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='ride_detail'),
    path('<uuid:pk>/start/', RideViewSet.as_view({'patch': 'start_ride'}), name='ride_start'),
    path('<uuid:pk>/complete/', RideViewSet.as_view({'patch': 'complete_ride'}), name='ride_complete'),
    path('<uuid:pk>/cancel/', RideViewSet.as_view({'patch': 'cancel_ride'}), name='ride_cancel'),
    path('accept_ride/', DriverViewSet.as_view({'post':'create'}), name='accept_ride')
]