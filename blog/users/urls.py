from django.urls import path
from .views import UserRegisterView, CustomLoginView, CustomLogoutView, UserEditView, ChangePasswordView, ShowProfileView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'users'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('edit_profile/', login_required(UserEditView.as_view()), name='edit-profile'),
    path('password-change/', ChangePasswordView.as_view(template_name='registration/change_password.html'), name='change-password'),
    path('password-success/', views.password_change_success, name='password-change-success'),
    path('<int:pk>/profile/', ShowProfileView.as_view(), name='show-profile'),
    path('<int:pk>/edit_profile_page/', login_required(EditProfilePageView.as_view()), name='edit-profile-page'),
    path('create_profile_page/', login_required(CreateProfilePageView.as_view()), name='create-profile-page'),
]
