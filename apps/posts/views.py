from django.shortcuts import render, redirect, HttpResponse
from django.views import View

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CreateSignalForm
from .models import Signal


class AddSignalView(View):
    form_class = CreateSignalForm
    template_name = 'posts/create.html'
    
    def get(self, request):
        context = {
            'form': self.form_class,
        }
        return render(request, self.template_name, context)
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            signal = form.save(user=request.user)
            messages.success(
                request,
                _("signal created successfuly!"),
                extra_tags="success",
            )
            return redirect('posts:details', signal.slug_title)
        
        return render(request, self.template_name, {'form': form})
    
    
class DetailSignalView(View):
    form_class = ...
    template_name = 'posts/details.html'
    
    def get(self, request, slug):
        signal = Signal.objects.get(slug_title=slug)
        
        context = {
            "signal": signal,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, slug): # comments
        pass
    
