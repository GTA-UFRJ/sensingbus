from django.contrib import admin

from .models import Measurement, Bus, Stop

admin.site.register(Measurement)
admin.site.register(Bus)
admin.site.register(Stop)