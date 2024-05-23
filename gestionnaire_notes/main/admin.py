from django.contrib import admin
from .models import Ressource, UE, RessourceUE, SAE, SaeUE

class RessourceUEInline(admin.TabularInline):
    model = RessourceUE
    extra = 1

class SaeUEInline(admin.TabularInline):
    model = SaeUE
    extra = 1

class RessourceAdmin(admin.ModelAdmin):
    inlines = (RessourceUEInline,)

class SaeAdmin(admin.ModelAdmin):
    inlines = (SaeUEInline,)

admin.site.register(Ressource, RessourceAdmin)
admin.site.register(SAE, SaeAdmin)
admin.site.register(UE)
