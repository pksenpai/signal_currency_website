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
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        pass
    

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
        print('$'*20, '001')
        form = self.form_class(request.POST)
        print('$'*20, '002')
        if form.is_valid():
            print('$'*20, '003')
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                print('$'*20, '004')
                login(request, user)
                messages.success(
                    request,
                    _(f"Welcome {request.user.username}!")
                )
                return redirect('core:home')
        
        messages.error(request, _("username or password is incorrect!"), extra_tags="danger")
        return render(request, self.template_name, {'form': form})
    
# class UserLoginView(LoginView):
#     template_name = 'users/login.html'
#     redirect_authenticated_user = True
        
#     def get_success_url(self):
#         username = self.request.POST.get("username")
#         if self.request.user.is_authenticated:
#             user = CustomUser.objects.get(username=username)
                
#             messages.success(
#                 self.request,
#                 _(
#                     # f"Login Successfuly. " \
#                     f"Welcome {user.username}!"
#                 )
#             )

#             next_url = self.request.GET.get('next')
#             if next_url:
#                 return next_url
#             return reverse_lazy('core:home')
#         return HttpResponseRedirect('users:login')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy("users:login")
    next_page = reverse_lazy("core:home")
    
    
