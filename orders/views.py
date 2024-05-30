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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

# Create your views here.


import logging

logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, slug):
        try:
            logger.debug("AddToCartView post method called")
            product = get_object_or_404(Product, slug=slug)
            logger.debug(f"Product found: {product}")
            
            order, created = Order.objects.get_or_create(user=request.user, created_at__isnull=False)
            logger.debug(f"Order found or created: {order}, created: {created}")
            
            quantity = int(request.POST.get('quantity', 1))
            logger.debug(f"Quantity from form: {quantity}")
            
            cart_item, created = CartItem.objects.get_or_create(order=order, product=product)
            if not created:
                cart_item.quantity += quantity
                logger.debug(f"Updated cart item quantity: {cart_item.quantity}")
            else:
                cart_item.quantity = quantity
                logger.debug(f"New cart item quantity: {cart_item.quantity}")
            cart_item.save()

            return HttpResponse(status=204)
            
        except Exception as e:
            logger.error(f"Error adding product to cart: {str(e)}", exc_info=True)
            return JsonResponse({'message': f"Error: {str(e)}"}, status=500)
    
    def get(self, request, slug):
        return JsonResponse({'message': 'Invalid request method'}, status=400)


class CartDetailView(TemplateView):
    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['cart/cart_auth.html']
        else:
            return ['cart/cart.html']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                order = Order.objects.get(user=request.user, created_at__isnull=False)
                cart_items = order.cartitem_set.all()
                total_price = order.total_price
            except Order.DoesNotExist:
                cart_items = []
                total_price = 0
            
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
                'user_authenticated': True
            }
        else:
            context = {
                'cart_items': [],
                'total_price': 0,
                'user_authenticated': False,
                'message': 'You need to sign in to purchase items.'
            }

        return self.render_to_response(context)     
    

@method_decorator(login_required, name='dispatch')
class ClearCartView(View):
    def post(self, request, *args, **kwargs):
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
        return redirect('orders:payment_complete')



@method_decorator(login_required, name='dispatch')
class PaymentCompleteView(TemplateView):
    template_name = 'payment/payment_completed.html'

    def get(self, request, *args, **kwargs):
        # Get the most recent order history for the user
        order_history = OrderHistory.objects.filter(user=request.user).order_by('-id').first()

        # Get the order history items associated with this order
        order_history_items = OrderHistoryItem.objects.filter(order_history=order_history)

        context = {
            'order_history': order_history,
            'order_history_items': order_history_items
        }

        return self.render_to_response(context)


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

