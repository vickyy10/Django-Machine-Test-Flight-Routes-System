from django.contrib import admin
from .models import Airport, Route

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city', 'country']
    search_fields = ['code', 'name', 'city']

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['from_airport', 'to_airport', 'position', 'distance']
    list_filter = ['position']
    search_fields = ['from_airport__code', 'to_airport__code']