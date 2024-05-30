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
from userprofile.models import UserProfile
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

                # Check if the user has provided an address
                user_has_address = hasattr(request.user, 'userprofile') and request.user.userprofile.address1 is not None
            except Order.DoesNotExist:
                cart_items = []
                total_price = 0
                user_has_address = False
            
            context = {
                'cart_items': cart_items,
                'total_price': total_price,
                'user_authenticated': True,
                'user_has_address': user_has_address  # Pass this variable to the template
            }
        else:
            context = {
                'cart_items': [],
                'total_price': 0,
                'user_authenticated': False,
                'message': 'You need to sign in to purchase items.'
            }

        return self.render_to_response(context)



@login_required
def pay_with_paypal(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # Check if the user has confirmed their address
    if not user_profile.address_confirmed:
        # Redirect the user to the address confirmation view
        return redirect('orders:confirm_address')  # Replace with the actual URL or URL name

    # Get the user's order and the associated cart items
    try:
        order = Order.objects.get(user=request.user, created_at__isnull=False)
        cart_items = order.cartitem_set.all()
        total_price = order.total_price
    except Order.DoesNotExist:
        cart_items = []
        total_price = 0

    # Render the PayPal payment view for the user
    response = render(request, 'payment/pay_with_paypal.html', {'cart_items': cart_items, 'total_price': total_price})

    # Handle the PayPal payment (not shown in this example)

    # Reset the address_confirmed attribute to False
    user_profile.address_confirmed = False
    user_profile.save()

    return response




@login_required
@login_required
def confirm_address(request):
    # Check if the user has items in their cart
    try:
        order = Order.objects.get(user=request.user, created_at__isnull=False)
        cart_items = order.cartitem_set.all()
        if not cart_items:
            # Redirect the user to the cart if it's empty
            return redirect('orders:cart_detail')  # Replace with the actual URL or URL name for the cart
    except Order.DoesNotExist:
        pass  # Handle the case where the order doesn't exist if needed

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Get the data from the form
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipcode = request.POST.get('zipcode')
        phone = request.POST.get('phone')

        # Update the user's profile
        user_profile.address1 = address1
        user_profile.address2 = address2
        user_profile.city = city
        user_profile.state = state
        user_profile.country = country
        user_profile.zipcode = zipcode
        user_profile.phone = phone
        user_profile.save()

        # Set the address_confirmed attribute to True
        user_profile.address_confirmed = True
        user_profile.save()

        # Redirect the user to the PayPal payment view
        return redirect('orders:pay_with_paypal')  # Replace with the actual URL or URL name

    # Render the form for the user
    return render(request, 'confirm/confirm_address.html', {'user_profile': user_profile})



    

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
        # Check if the user has any recent orders
        try:
            order_history = OrderHistory.objects.filter(user=request.user).order_by('-id').first()
            if not order_history:
                # Redirect the user to a relevant page if there are no recent orders
                return redirect('orders:cart_detail')  # Replace with the actual URL or URL name for the cart
        except OrderHistory.DoesNotExist:
            # Redirect the user to a relevant page if there are no recent orders
            return redirect('orders:cart_detail')  # Replace with the actual URL or URL name for the cart

        # Get the order history items associated with this order
        order_history_items = OrderHistoryItem.objects.filter(order_history=order_history)

        # Check if there are any items in the order history
        if not order_history_items:
            # Redirect the user to a relevant page if there are no items in the order
            return redirect('orders:cart_detail')  # Replace with the actual URL or URL name for the cart

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
    model = OrderHistory  # Use the OrderHistory model
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

