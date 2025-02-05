from django.urls import path
from .views import user_login, dashboard_view, user_register
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetView, PasswordResetCompleteView
from .views import CustomPasswordResetView, SingupView, edit_user, EditUserView

urlpatterns = [
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', PasswordChangeView.as_view(), name="password_change"),
    path("password-change-done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
    # path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("password-reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password-reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),    
    path("password-reset/complete", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('profile/', dashboard_view, name='user_profile'),
    path("singup/", user_register, name="user_register"),
    # path("singup/", SingupView.as_view(), name="user_register"),
    # path("profile/edit/", edit_user, name="edit_user_information"),
    path("profile/edit/", EditUserView.as_view(), name="edit_user_information"),
]

