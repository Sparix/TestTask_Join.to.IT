from django.contrib import admin

from EvenAPI.models import Event, JoinEvent


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "organizer", "count_place")

@admin.register(JoinEvent)
class JoinEventAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "registered_at")
