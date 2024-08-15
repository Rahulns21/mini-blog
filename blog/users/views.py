from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .forms import SignUpForm, EditProfilePageForm
from django.contrib.auth.views import LoginView as AuthLoginView, LogoutView as AuthLogoutView
from django.urls import reverse_lazy
from .forms import EditProfileForm, ChangePasswordForm, CreateProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from myblog.models import UserProfile

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:login')

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('myblog:home')  # Change 'home' to your desired URL name
        return super().dispatch(*args, **kwargs)
    
class CustomLoginView(AuthLoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('myblog:home')  # Change 'home' to your desired URL name

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(*args, **kwargs)
    
class CustomLogoutView(AuthLogoutView):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('myblog:home'))  # Redirect to home if user is not logged in
        return super().dispatch(*args, **kwargs)
    
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('myblog:home')

    def get_object(self):
        return self.request.user

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('users:password-change-success')

@login_required
def password_change_success(request):
    context = {}
    return render(request, 'registration/password_change_success.html', context=context)

class ShowProfileView(generic.DetailView):
    model = UserProfile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfileView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(UserProfile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context
    
class EditProfilePageView(generic.UpdateView):
    model = UserProfile
    form_class = EditProfilePageForm
    template_name = 'registration/edit_profile_page.html'
    success_url = reverse_lazy('myblog:home')

class CreateProfilePageView(generic.CreateView):
    model = UserProfile
    form_class = CreateProfileForm
    template_name = 'registration/create_profile.html'
    success_url = reverse_lazy('myblog:home')

    def dispatch(self, *args, **kwargs):
        # Check if the user already has a profile
        if hasattr(self.request.user, 'userprofile'):
            # Redirect to the profile page if it already exists
            return redirect('users:show-profile', self.request.user.userprofile.id)
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form) 