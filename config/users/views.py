from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import  TemplateView, CreateView, UpdateView, ListView, DeleteView
import secrets
from .forms import UserRegisterForm, UserProfileForm
from .models import User
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .achievements import ACHIEVEMENTS

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        user.token = token
        user.save()
        send_mail(
            'Подтверждение почты',
            f'Перейдите по ссылке для подтверждения почты {url}',
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


# class ProfileView(LoginRequiredMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     success_url = reverse_lazy('users:user_form')
#
#     def get_object(self, queryset=None):
#         return self.request.user


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'view_user_list'
    template_name = 'users/user_list.html'


class UserDeleteView(PermissionRequiredMixin, DeleteView):
    model = User
    permission_required = 'block_user'
    success_url = reverse_lazy('users:users')
    template_name = 'users/users_confirm_delete.html'


class ResetView(PasswordResetView):
    model = User
    template_name = 'users/resetview.html'
    email_template_name = 'users/password_reset_email.html'

    success_url = reverse_lazy('service:homepage')


class PasswordResetDone(PasswordResetDoneView):
    model = User
    template_name = 'users/password_reset_done.html'


class ResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:complete')


class ResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


@login_required
def profile(request):
    if request.method == 'POST':
        # Обновление данных
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone = request.POST.get('phone', '')
        user.country = request.POST.get('country', '')

        # Обработка аватара
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        return redirect('users:profile')

    # GET — рендерим форму + достижения
    return render(request, 'users/profile.html', {
        'achievements': ACHIEVEMENTS,
    })


class ProfileView(TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['achievements'] = ACHIEVEMENTS
        return ctx
