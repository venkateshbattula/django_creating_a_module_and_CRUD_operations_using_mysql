from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.


def delete_employees_for_location(modeladmin, request, queryset):
    for obj in queryset:
        emp_list = obj.employee_set.all()
        for emp in emp_list:
            emp.delete()


delete_employees_for_location.short_description = "Delete Employees of selected locations"


class LocationAdmin(admin.ModelAdmin):
    search_fields = ['state']

    def delete_queryset(self, request, queryset):
        for loc in queryset:
            loc.delete()
    actions = [delete_employees_for_location]


admin.site.register(Location, LocationAdmin)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'location__state', 'gender']
    list_display = ['name', 'gender', 'package', 'location', 'image_display']

    def image_display(self, obj):
        return format_html("<img src='{}' width='100' height='100' />".format(obj.photo.url))

    def delete_queryset(self, request, queryset):
        for emp in queryset:
            emp.delete()

    image_display.short_description = 'Employee_Photo'


