from rest_framework import viewsets, status
from .models import Ride
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from drf_yasg.utils import swagger_auto_schema


from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Ride
from .serializers import LogInSerializer, NestedTripSerializer, UserSerializer, TripSerializer


class SignUpView(generics.CreateAPIView):
    parser_classes = [MultiPartParser, FormParser]

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()  


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()  


class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NestedTripSerializer

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        ride = self.get_object()
        serializer = self.get_serializer(ride)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_request(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(rider=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        if user.group == 'driver':
            return Ride.objects.filter(
                Q(status=Ride.REQUESTED) | Q(driver=user)
            )
        if user.group == 'rider':
            return Ride.objects.filter(rider=user)
        return Ride.objects.none()

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()  
    


# from .serializers import RideSerializer


# class RideViewSet(viewsets.ModelViewSet):
#     queryset = Ride.objects.all()
#     serializer_class = RideSerializer

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = TripSerializer


    @action(detail=True, methods=['patch'])
    def start_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status != Ride.REQUESTED:
            return Response({'error': 'Ride is not in requested status'}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = Ride.IN_PROGRESS
        ride.save()
        serializer = self.get_serializer(ride)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def complete_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status != Ride.IN_PROGRESS:
            return Response({'error': 'Ride is not in progress status'}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = Ride.COMPLETED
        ride.save()
        serializer = self.get_serializer(ride)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def cancel_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status in [Ride.COMPLETED, Ride.CANCELLED]:
            return Response({'error': 'Ride cannot be cancelled as it is already completed or cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = Ride.CANCELLED
        ride.save()
        serializer = self.get_serializer(ride)
        return Response(serializer.data)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers()  

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = TripSerializer

    @action(detail=True, methods=['post'])
    def accept_ride(self, request, pk=None):
        ride = self.get_object()

        if ride.status != 'REQUESTED':
            return Response({'error': 'Ride has already been accepted'}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_driver:
            return Response({'error': 'Only drivers can accept rides'}, status=status.HTTP_403_FORBIDDEN)

        available_drivers = Ride.objects.filter(driver=None)
        if not available_drivers.exists():
            return Response({'error': 'No available drivers'}, status=status.HTTP_404_NOT_FOUND)

        driver = available_drivers.first()
        ride.driver = driver
        ride.status = 'ACCEPTED'
        ride.save()

        return Response({'message': 'Ride accepted successfully'}, status=status.HTTP_200_OK)

    def get_parsers(self):
        if getattr(self, 'swagger_fake_view', False):
            return []
        return super().get_parsers() 