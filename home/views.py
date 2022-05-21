from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_safe


@require_safe
def home(request):
    context = None
    return render(request, 'home/home.html', context)
