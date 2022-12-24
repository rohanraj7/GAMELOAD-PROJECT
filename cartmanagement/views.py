from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from gameadmin.models import Categories
from cartmanagement.models import wishlist,Guestcart
from gameuser.views import login_view, view_home
from productmanagement.models import Stock
from .models import Cart

# Create your views here.




@never_cache
def view_cart(request):
    if request.user.is_authenticated:
        ob = Cart.objects.filter(userid=request.user.id).order_by('id')
        onj = Categories.objects.values('offer')

        
        total=0
        for j in ob:

            total = total + j.amount

            t=total*100
        context={'total':total,'ob':ob} 
        return render(request, 'mycart.html', context)
    else:
        if not request.session.session_key:
            request.session.create()
        request.session['guest_key']=request.session.session_key
        key = request.session['guest_key']        
        print(request.session.session_key)
        ob=Guestcart.objects.filter(userreference=request.session.session_key)
        total=0
        for j in ob:
            total = total +j.amount
        context = {'total':total,'ob':ob}
        return render(request, 'mycart.html',context)    


def remove_cart(request,id):
    if request.user.is_authenticated:
        o = Cart.objects.get(id=id)
        o.delete()
        n = 'Product Removed from cart'
        messages.info(request,n)
    else:
        ob = Guestcart.objects.get(id=id)
        ob.delete()
        n = 'Product Removed from cart'
        messages.info(request,n)       
    return redirect(view_cart)

def dquantity(request):
    if request.user.is_authenticated and request.user.is_active:
        
        if request.method =="POST":    
            id = request.POST['id']
            car = Cart.objects.get(id=id)
            cart = Cart.objects.get(id=id)
            ob=Cart.objects.values('quantity').get(id=id)
            quantity = ob['quantity']
            if quantity >= 2:


                Cart.objects.filter(id=id).update(quantity=ob['quantity']-1)
            ob=Cart.objects.values('quantity').get(id=id)
            o=Cart.objects.values('quantity','price','amount').get(id=id)
            Cart.objects.filter(id=id).update(amount=o['price']*o['quantity'])

            Cart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Cart.objects.values('quantity','price','amount').get(id=id)
            
            cart = Cart.objects.filter(userid=request.user)
            

            amount = o['amount']
            q =ob['quantity']
            total = 0
            for j in cart:
            
                total = total + j.amount
            cart1 = car.productid.stock
        return JsonResponse({'amount':amount,'q':q,'total':total,'cart1':cart1})      #type:ignore

    else:
        if request.method =="POST":
            id = request.POST['id']
            car = Guestcart.objects.get(id=id)
            ob=Guestcart.objects.values('quantity').get(id=id)
            quantity = ob['quantity']
            if quantity >= 2:

                Guestcart.objects.filter(id=id).update(quantity=ob['quantity']-1)
            ob=Guestcart.objects.values('quantity').get(id=id)
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)
            Guestcart.objects.filter(id=id).update(amount=o['price']*o['quantity'])

            Guestcart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)

            amount = o['amount']
            q =ob['quantity']

            cart = Guestcart.objects.filter(userreference=request.session.session_key)
            total = 0
            for j in cart:
                total = total + j.amount
            cart1 = car.productid.stock    
        return JsonResponse({'amount':amount,'q':q,'total':total,'cart1':cart1})      #type:ignore
                
@csrf_exempt
def iquantity(request):
    if request.user.is_authenticated and request.user.is_active:
        if request.method =="POST":
            id = request.POST['id']
            car = Cart.objects.get(id=id)
            print(car.productid.stock)
            ob=Cart.objects.values('quantity').get(id=id)

            Cart.objects.filter(id=id).update(quantity=ob['quantity']+1)
            ob=Cart.objects.values('quantity').get(id=id)
            o=Cart.objects.values('quantity','price','amount').get(id=id)

            Cart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Cart.objects.values('quantity','price','amount').get(id=id)

            amount = o['amount']
            q =ob['quantity']
            cart = Cart.objects.filter(userid=request.user)
            total = 0
            for j in cart:
            
                total = total + j.amount
            cart1 = car.productid.stock   
            print(cart1) 
        return JsonResponse({'amount':amount,'q':q,'total':total,'cart1':cart1})  #type:ignore
    else:
        if request.method =="POST":
            id = request.POST['id']
            car = Guestcart.objects.get(id=id)
            ob=Guestcart.objects.values('quantity').get(id=id)

            Guestcart.objects.filter(id=id).update(quantity=ob['quantity']+1)
            ob=Guestcart.objects.values('quantity').get(id=id)
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)

            Guestcart.objects.filter(id=id).update(amount=o['price']*o['quantity'])
            o=Guestcart.objects.values('quantity','price','amount').get(id=id)

            amount = o['amount']
            q =ob['quantity']
            cart = Guestcart.objects.filter(userreference=request.session.session_key)
            total = 0
            for j in cart:
            
                total = total + j.amount
            cart1=car.productid.stock
        return JsonResponse({'amount':amount,'q':q,'total':total,'cart1':cart1})      #type:ignore

def view_wishlist(request):
    if request.user.is_authenticated:
        wish = wishlist.objects.filter(user=request.user)
        context = {'wish':wish}
        return render(request,'wishlist.html',context)
    return redirect(login_view)



def add_wishlist(request,id):
    if request.user.is_authenticated:
        s = Stock.objects.all().get(id=id)
        w = wishlist.objects.all()
    
        if wishlist.objects.filter(productid=s ,user=request.user).exists():
            n='Added to Wishlist'
            messages.info(request,n)
            return redirect(view_home)
        else:
            add = wishlist(productname = s.name, user=request.user,productid=s, description = s.description, image = s.image1,price=s.price)

            add.save()
            n='Added to Wishlist'
            messages.info(request,n)
    else:
        return redirect(login_view)
    return redirect(view_home)

def remove_wishlist(request,id):
    w = wishlist.objects.get(id=id)
    w.delete()
    n = 'Product Removed from wishlist'
    messages.success(request,n)
    return redirect(view_wishlist)    
   