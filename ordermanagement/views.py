from datetime import datetime
from django.shortcuts import redirect,render
from django.views.decorators.cache import never_cache
from django.contrib import messages
from gameadmin.models import Coupon, Myorders
from productmanagement.models import Stock
from gameuser.views import login, login_view
from cartmanagement.models import Cart
from cartmanagement.views import view_cart
from django.contrib.auth.models import User
from gameadmin.models import Address,Payment
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
from django.http import JsonResponse

# Create your views here.


@never_cache
def checkout(request):
    if request.user.is_authenticated:
        try:
            cart2 = Cart.objects.filter(userid=request.user.id)
        except:
            cart2= None
        try:
            cart = Cart.objects.get(userid=request.user.id)
        except:
            cart = None
        if not cart2 and cart is None:
            return redirect(success_cash)
        

        add = Address.objects.filter(user=request.user)
        ob = Cart.objects.values().filter(userid=request.user.id)
        total=0
        m=0
        for j in ob:
            
            total = total + j['amount']

            m = total*100
        
        request.session['money']=m
        request.session['t']=total
        ord2 = str(datetime.now())+str(request.user.id)
        ord1 = ord2.translate({ord(':'): None,ord('-'): None, ord(' '): None, ord('.'): None})
        request.session['neworderid'] = ord1
        apply_coupon = Coupon.objects.values('coupon_code')
        now = datetime.now()
        
        # COUPONS
        if 'coupons' in request.GET:
            code = request.GET['coupon']
            try:
                coup = Coupon.objects.get(coupon_code=code,added_date__lt=now,validtill__gt=now,minimum_price__lt=total)
                request.session['coupon_offer'] = coup.discount
                request.session['coupon_code'] =coup.coupon_code
                if request.session['coupon_offer'] is not None:
                    total = total-(total*request.session['coupon_offer'])/100
                    n = ' Coupon APPLIED successfully '
                    messages.success(request,n)
            except Coupon.DoesNotExist:
                n = 'ENTER VALID COUPON'
                messages.info(request,n)
                return redirect(checkout)        

        if request.method=='POST':
            Name     = request.POST['name']
            address  = request.POST['address']
            method   = request.POST['method']
            y = Address.objects.get(id=address)

            for i in ob:
                obj = Stock.objects.get(id=i['productid_id'])
                if obj.stock >= i['quantity']:

                    s = Myorders(userid =request.user,name=Name, address=y,method=method,productid=obj,orderid=ord1,productname=i['productname'],amount=i['price'],quantity=i['quantity'],image=i['image'],totalamount=i['amount'])
                    s.save()
                    Stock.objects.filter(id=i['productid_id']).update(stock=(obj.stock-i['quantity']))
                else:
                    messages.warning(request,' PRODUCT OUT OF STOCK')
                    return redirect(checkout)
                
                
                
                
            if request.POST['method']=='razorpay':
                amount=50000
                order_currency = 'INR'
                client = razorpay.Client(
                        auth=('rzp_test_SwupBK06DEvv6V', 'P6DCiW5gkQke1e4uxcTkE5VE')
                        )

                payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'0'})  # type: ignore
                payment_id = payment['id']
                request.session['payment']= payment
                payment_status = payment['status']
                
                if payment_status == 'created':
                    return render(request, "razorpay.html", {'payment': payment, 'm' : amount, "ob":ob, "total":total,'ord1':ord1 })
                # return render(request, "razorpay.html")
                return redirect(checkout)
                
            elif request.POST['method']=='paypal':
                amount=request.session['money']
                orderid = request.session['neworderid']
                context= {'total':total,'orderid':orderid,'ob':ob,'m':amount,'ord1':ord1 }
                de = Cart.objects.filter(userid=request.user.id)
                de.delete()
                return render(request,'paypal.html', context)
              
            else:
                de = Cart.objects.filter(userid=request.user.id)
                de.delete()
                return render(request,'success1.html')
        return render(request,'checkout.html',{'ob':ob,'applycoupon':apply_coupon,'m':m, 'total':total, 'add':add})
    else:
        return redirect(login_view)

def myorder(request):
    if request.user.is_authenticated:

        ob = Myorders.objects.filter(userid=request.user.id).order_by('-id')
        context = {'ob':ob}
        return render(request, 'myorder.html',context)
    else:
        return redirect(login)    
  


def cancel_order(request,id):
    if request.user.is_authenticated:
        obj = Myorders.objects.values('status','orderstatus').get(id=id)
   
        if obj['orderstatus']=='Placed':
            if obj['status']==True:
                Myorders.objects.filter(id=id).update(status=False)
            n='order cancelled'
            messages.info(request,n)
            return redirect(myorder)
        else:
            return redirect(myorder)
    else:
        
        return redirect(myorder)     

@csrf_exempt
def success(request):
        response=request.POST
        order_ins = Myorders.objects.values('orderid').filter(userid_id=request.user)
        
        total = request.session['t']
        neworderid = request.session['neworderid']
        
        params_dict = {
            'razorpay_payment_id' : response['razorpay_payment_id'],
            'razorpay_order_id' : response['razorpay_order_id'],
            'razorpay_signature' : response['razorpay_signature'],
        }
        
        
        ins = Payment(user=request.user, paymentid=params_dict["razorpay_payment_id"], paymentmethod='razor', totalamount=total,status='paid',
                    orderid=neworderid)
        ins.save()
        pay = Payment.objects.filter(orderid=request.user)

        client = razorpay.Client(auth=("rzp_test_SwupBK06DEvv6V", "P6DCiW5gkQke1e4uxcTkE5VE"))
        de = Cart.objects.filter(userid=request.user.id)
        de.delete() 
        try:
            client.utility.verify_payment_signature(params_dict)  # type: ignore

            return render(request, 'success1.html')
        except:
            return render(request, 'success1.html')


def success_cash(request):
    return render(request,'success1.html')




def return_item(request,id):
    order = Myorders.objects.get(id=id)
    order.orderstatus = "Return Pending" 
    order.save()
    print(order.orderstatus)
    return redirect('myorder')

        


