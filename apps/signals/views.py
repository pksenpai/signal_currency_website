from django.shortcuts import render, redirect, reverse
from django.views import View

from .forms import CreateSignalForm
from .models import Signal


class AddSignalView(View):
    form_class = CreateSignalForm
    template_name = 'signals/create.html'
    
    def get(self, request):
        context = {
            'form': self.form_class,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        signal = self.form_class(request.POST)
        if signal.is_valid():
            clean_signal: dict = signal.cleaned_data
            clean_signal.save(user=request.user)
            
            # clean_signal['author'] = request.user
            # Signal.objects.create(clean_signal) # another way to save data
            
            messages.success(
                request,
                _(
                    "Signal created successfuly!"
                )
            )
            return redirect('core:home')
        
        messages.error(request, _("Signal did NOT create!"), extra_tags="danger")
        return reverse("signals:add")

            
            
            