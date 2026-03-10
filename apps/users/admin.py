from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms  # <-- 1. Import forms
from .models import User

# 2. Create a custom form for adding users in the admin panel
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'is_active', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        # Give them an unusable password since they will use OTP
        user.set_unusable_password() 
        if commit:
            user.save()
        return user

class CustomUserAdmin(UserAdmin):
    model = User
    
    # 3. Tell the admin to use your new custom form for the "Add user" page
    add_form = CustomUserCreationForm 
    
    # ... Keep all your existing settings below this point ...
    list_display = ('phone', 'username', 'email', 'is_active', 'is_staff', 'created_at')
    list_filter = ('is_active', 'is_staff', 'created_at')
    search_fields = ('phone', 'username', 'email')
    ordering = ('-created_at',)

    fieldsets = (
        ('Login Credentials', {'fields': ('phone',)}),
        ('Personal Info', {'fields': ('username', 'email', 'bio')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('id', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'is_active', 'is_staff')}
        ),
    )

    readonly_fields = ('id', 'created_at', 'updated_at')

admin.site.register(User, CustomUserAdmin)