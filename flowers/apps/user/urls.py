from django.urls import path

from . import views

urlpatterns = [
    path('', views.ChangePassword.as_view(), name='user'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('delete/', views.delete_account, name='delete-account'),
    path('security/', views.user_security, name='security'),
    path('personal/', views.user_personal, name='personal'),
    path('verify/', views.verify_code, name='verify'),
]
