from django.contrib import admin

from . import models

class PitchInline(admin.TabularInline):
    model = models.Pitch

class RouteAdmin(admin.ModelAdmin):
    inlines = (
        PitchInline,
    )

admin.site.register(models.Route, RouteAdmin)

admin.site.register(models.Attempt)
admin.site.register(models.Boulder)
admin.site.register(models.Todo)
