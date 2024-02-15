from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, register, edit, user_logout

urlpatterns = [
    # path('login/', user_login, name='login'),
    
    # url-адреси для входу та виходу
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    
    # url-адреси для зміни пароля
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uuid64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset'),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
        
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
]