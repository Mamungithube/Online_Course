from django.contrib import admin
from . import models

class CatagoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }
    
admin.site.register(models.Catagory, CatagoryAdmin)
admin.site.register(models.Teacher)
admin.site.register(models.Review)