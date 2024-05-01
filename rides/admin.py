from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import Ride, User


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    fields = (
        'id', 'pickup_location', 'dropoff_location', 'status',
        'driver', 'rider',
        'created', 'updated',
    )
    list_display = (
        'id', 'pickup_location', 'dropoff_location', 'status',
        'driver', 'rider','created_at', 'updated_at',
    )
    list_filter = (
        'status',
    )
    readonly_fields = (
        'id', 'created_at', 'updated_at',
    )

