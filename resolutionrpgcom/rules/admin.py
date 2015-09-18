from django.contrib import admin

# Register your models here.

# TRAIT #
from .models import Trait

class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'value')
    fieldsets = [
        (None,          {'fields': ['name']}),
        (None,          {'fields': [('short_description')], 'classes': ['wide']}),
    ]

admin.site.register(Trait, TraitAdmin)