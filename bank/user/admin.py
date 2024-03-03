from django.contrib import admin
from .models import User, Department, SubDepartment, Section, Organization, Criterion
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import redirect

# Inline Admin for Departments
class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    fields = ('name', 'department_percentage', 'achieved_percentage')
    readonly_fields = ('department_percentage', 'achieved_percentage')

# Admin Action for updating achieved percentage
@admin.action(description='🔄 Update Achieved Percentage')
def update_achieved_percentage_action(modeladmin, request, queryset):
    for obj in queryset:
        obj.update_achieved_percentage()
    modeladmin.message_user(request, f"Achieved percentages updated for {queryset.count()} selected objects.")

# Department Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user/department/change_list.html'    
    list_display = ['name', 'department_percentage', 'achieved_percentage']
    
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update-achieved/', self.admin_site.admin_view(self.update_achieved_percentage), name='update-achieved-percentage'),
        ]
        return my_urls + urls

    def update_achieved_percentage(self, request):
        # Implement the logic to update the achieved percentage
        queryset = Department.objects.all()
        for obj in queryset:
            obj.update_achieved_percentage()  # Assuming this is a method on your Department model
        self.message_user(request, "Achieved percentages updated successfully.")
        return HttpResponseRedirect("../")

# SubDepartment Admin
@admin.register(SubDepartment)
class SubDepartmentAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user/subdepartment/change_list.html'
    list_display = ['name', 'sub_department_percentage', 'achieved_percentage']
    readonly_fields = ['achieved_percentage']
    search_fields = ['name']
    # actions = [update_achieved_percentage_action]  # Remove this if you are replacing with a button

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update-achieved/', self.admin_site.admin_view(self.update_achieved_percentage), name='subdepartment-update-achieved-percentage'),
        ]
        return custom_urls + urls

    def update_achieved_percentage(self, request):
        queryset = self.model.objects.all()
        for obj in queryset:
            obj.update_achieved_percentage()
        self.message_user(request, "Achieved percentages updated successfully for subdepartments.")
        return HttpResponseRedirect("../")

# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'is_staff']
    search_fields = ['email', 'name']
    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new user
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

# Section Admin
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user/section/change_list.html'
    list_display = ['section_name', 'actual_percentage', 'achieved_percentage']
    readonly_fields = ['achieved_percentage']
    list_filter = ['related_sub_department']
    search_fields = ['section_name']
    # actions = [update_achieved_percentage_action]  # Remove this if you are replacing with a button

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('update-achieved/', self.admin_site.admin_view(self.update_achieved_percentage), name='section-update-achieved-percentage'),
        ]
        return custom_urls + urls

    def update_achieved_percentage(self, request):
        queryset = self.model.objects.all()
        for obj in queryset:
            obj.update_achieved_percentage()
        self.message_user(request, "Achieved percentages updated successfully for sections.")
        return HttpResponseRedirect("../")

# Organization Admin
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_departments_details']
    def get_departments_details(self, obj):
        departments_details = [f"{dept.name} - Actual: {dept.department_percentage}%, Achieved: {dept.achieved_percentage}%" for dept in obj.departments.all()]
        return "; ".join(departments_details)
    get_departments_details.short_description = 'Departments Details'

# Criterion Admin
@admin.register(Criterion)
class CriterionAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'is_checked', 'attached_file', 'points']
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ['points', 'name', 'section']
        return super().get_readonly_fields(request, obj)
