
from multiprocessing import AuthenticationError
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import logout
from django.views.generic import ListView
from products.models import *
from django.shortcuts import render, get_object_or_404
from orders.models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import *
# Create your views here.

# create sign in view for me 
class SignInView(View):
    def get(self, request):
        return render(request, 'auth/sign_in.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home:home_auth') 
        else:
            return HttpResponse("Invalid login credentials. Please try again.")
        


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'