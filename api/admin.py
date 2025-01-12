from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hobby

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'date_of_birth', 'hobbies')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Relationships', {'fields': ('friends',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    def save_model(self, request, obj, form, change):
        """
        Overrides the default save method to hash the password if it is not already hashed.
        """
        if form.cleaned_data.get('password') and not obj.password.startswith('pbkdf2_'):
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
