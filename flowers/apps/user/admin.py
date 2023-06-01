from django.contrib import admin

from apps.user.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'bio', 'birth_date', 'profile_img', 'country', 'city', 'phoneNumber',
                    'is_phone_verified', 'balance']
