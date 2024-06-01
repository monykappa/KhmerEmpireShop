from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout


# Create your views here.

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    login_url = reverse_lazy('dashboard:sign_in') 

class DashboardSignInView(LoginView):
    template_name = 'dashboard/sign_in.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return reverse_lazy('dashboard:dashboard')

class DashboardLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('dashboard:sign_in')
