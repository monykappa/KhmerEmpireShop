
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
from django.views.generic import DetailView


class HomeView(TemplateView):
    template_name = 'home/home.html'

class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'base.html'

class HomeAuth(LoginRequiredMixin, TemplateView):
    def get(self, request):
        template = 'home/home_auth.html'
        return render(request, template)
    
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
        


class ProductListView(LoginRequiredMixin, ListView):
    model = LaptopSpec
    template_name = 'products/products.html'
    context_object_name = 'laptop_specs'

def product_detail(request, slug):
    laptop_spec = get_object_or_404(LaptopSpec, slug=slug)
    print(laptop_spec)  # Add this debug print
    return render(request, 'products/products_detail.html', {'laptop_spec': laptop_spec})


@login_required
def add_to_cart(request, slug):
    if request.method == "POST":
        try:
            product = get_object_or_404(Product, slug=slug)
            order, created = Order.objects.get_or_create(user=request.user, created_at__isnull=False)
            
            quantity = int(request.POST.get('quantity', 1))  # Get quantity from form, default to 1 if not provided
            
            cart_item, created = CartItem.objects.get_or_create(order=order, product=product)
            if not created:
                cart_item.quantity += quantity  # Add the specified quantity
            else:
                cart_item.quantity = quantity  # Set the specified quantity if item is newly created
            cart_item.save()

            return HttpResponse(status=204)  # No Content
            
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    
    return JsonResponse({'message': 'Invalid request'}, status=400)


@login_required
def cart_detail(request):
    try:
        order = Order.objects.get(user=request.user, created_at__isnull=False)
        cart_items = order.cartitem_set.all()
        total_price = order.total_price
    except Order.DoesNotExist:
        cart_items = []
        total_price = 0
    
    return render(request, 'home/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def clear_cart(request):
    # Get cart items
    cart_items = CartItem.objects.filter(order__user=request.user)
    
    # Calculate total
    total = sum(item.subtotal for item in cart_items)
    
    # Create OrderHistory
    order_history = OrderHistory.objects.create(
        user=request.user, 
        total_price=total
    )

    # Save items
    for item in cart_items:
        OrderHistoryItem.objects.create(
            order_history=order_history,
            product=item.product,
            quantity=item.quantity,
            subtotal=item.subtotal
            )

    # Clear cart 
    CartItem.objects.filter(order__user=request.user).delete()

    # Redirect
    return redirect('home:payment_complete') 

def payment_complete(request):
    # Get the most recent order history for the user
    order_history = OrderHistory.objects.filter(user=request.user).order_by('-id').first()

    # Get the order history items associated with this order
    order_history_items = OrderHistoryItem.objects.filter(order_history=order_history)

    return render(request, 'payment/payment_completed.html', {'order_history': order_history, 'order_history_items': order_history_items})



class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/profile.html'

class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = 'order/order_history.html'
    model = OrderHistory
    context_object_name = 'orders'

    def get_queryset(self):
        return OrderHistory.objects.filter(user=self.request.user).order_by('-ordered_date')

class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'order/order_detail.html'
    model = OrderHistory
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home:home')