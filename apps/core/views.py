from apps.posts.models import Signal

from django.views import View

from django.shortcuts import render
from django.db.models import Q


class Home(View):
    template_name = 'core/home.html'
    
    def get(self, request):
        if searched:=request.GET.get('searched'):
            searched: str = searched.strip()
            signals = Signal.objects.filter(Q(title__icontains=searched) | Q(summary__icontains=searched))
        else:            
            signals = Signal.objects.all()

        context = {
            'signals': signals
        }
        
        return render(request, self.template_name, context)

