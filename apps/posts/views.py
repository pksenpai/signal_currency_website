from django.shortcuts import render, redirect, HttpResponse
from django.views import View

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import CreateSignalForm


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
            form.save(user=request.user)
            messages.success(
                request,
                _("signal created successfuly!"),
                extra_tags="success",
            )
            return redirect('core:home') # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        return render(request, self.template_name, {'form': form})
    
class DetailSignalView(View):
    
    def get(self, request, slug):
        return HttpResponse("Hello world!")
    
    def post(self, request, slug): # comments
        pass
    
    