# CREATE CUSTOMER ORDER
# 1.Present a user with an order form to fill in their data
# 2.Create a new Order instance with the data entered, and create an associated OrderItem instance
# for each item in the cart
# 3.Clear all the cart’s contents and redirect the user to a success page

from .tasks import order_created
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.urls import reverse


def order_create(request):
    cart = Cart(request)    # get current cart from the SESSION.
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch async task
            order_created.delay(order.id) # Task is added to the message queue and executed by celery worker as soon as possible.
            # SET ORDER IN THE SESSION
            request.session['order_id'] = order.id
            # payment redirect
            return redirect(reverse('payment:process'))



    else:
        form = OrderCreateForm()
        return render(request, 
                      'orders/order/create.html',
                      {'cart': cart, 'form':form})
    
# Admin panel view
@staff_member_required # is_active and is_staff both true
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 
                  'admin/orders/order/detail.html',
                  {'order': order})








#