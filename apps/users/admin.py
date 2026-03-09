from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    
    # What columns are shown on the main user list page
    list_display = ('phone', 'username', 'email', 'is_active', 'is_staff', 'created_at')
    
    # What fields you can filter the list by (right sidebar)
    list_filter = ('is_active', 'is_staff', 'created_at')
    
    # What fields the search bar will look through
    search_fields = ('phone', 'username', 'email')
    
    # Default sorting (newest users first)
    ordering = ('-created_at',)

    # How fields are grouped when you click on a specific user to edit them
    fieldsets = (
        ('Login Credentials', {'fields': ('phone',)}),
        ('Personal Info', {'fields': ('username', 'email', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('id', 'created_at', 'updated_at')}),
    )

    # How fields are grouped when you click "Add User" in the admin dashboard
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'is_active', 'is_staff')}
        ),
    )

    # Make the UUID and timestamps read-only so they can't be accidentally edited
    readonly_fields = ('id', 'created_at', 'updated_at')

# Register the model and the custom admin class
admin.site.register(User, CustomUserAdmin)