from django.contrib import admin

# Register your models here.
from core.models import Todo
# from core.models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Todo, TodoAdmin)
