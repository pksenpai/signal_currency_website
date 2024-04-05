from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import UserRegisterForm, UserLoginForm
from .models import CustomUser, Profile


class UserSignupView(View):
    form_class = UserRegisterForm
    template_name = 'users/signup.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            context = {
                'form': self.form_class
            }
            return render(request, self.template_name, context)
        return redirect('core:home')
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(
                request,
                _(
                    f"congratulations {request.user.username}!" \
                    "your account created successfuly!"
                ),
                extra_tags="success"
            )
            
            messages.info(
                request,
                _(f"I suggest you complete your profile"),
                extra_tags="info"
            )
            
            return redirect('users:login')
        
        return render(request, self.template_name, {'form': form})
        

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            context = {
                'form': self.form_class,
            }
            return render(request, self.template_name, context)
        return redirect('core:home')
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(
                    request,
                    _(f"Welcome {request.user.username}!")
                )
                return redirect('core:home')
        
        messages.error(request, _("username or password is incorrect!"), extra_tags="danger")
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy("users:login")
    next_page = reverse_lazy("core:home")
    
    
