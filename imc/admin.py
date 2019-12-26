from django.contrib import admin
from .models import Imc, WeightHistory, Profile

class ImcAdmin(admin.ModelAdmin):
    readonly_fields = ('imc', 'classificacao')


admin.site.register(Imc, ImcAdmin)
admin.site.register(WeightHistory)
admin.site.register(Profile)
