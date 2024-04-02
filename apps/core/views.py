from apps.signals.models import Signal

from django.views import View

from django.shortcuts import render


class Home(View):
    template_name = 'core/home.html'
    
    def get(self, request):
        signals = Signal.objects.all()
        context = {
            'signals': signals
        }
        
        return render(request, self.template_name, context)

