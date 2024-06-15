from django.contrib import admin

from .models import Instrument, Strategy

admin.site.register(Strategy)
admin.site.register(Instrument)
