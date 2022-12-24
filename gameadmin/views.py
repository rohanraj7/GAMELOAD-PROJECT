from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate,login
from gameadmin.models import Coupon, Payment, User,Myorders
from django.contrib import messages
from cartmanagement.models import Cart
from django.contrib.auth import logout
from django.db.models import Q
from productmanagement.models import Stock
from django.utils import timezone
from django.db.models import Sum
import datetime
from datetime import date
from django.db.models.functions import TruncMonth
from django.db.models import Count
# from gameadmin.models import Categories 
# Create your views here.




@never_cache
def adminlogin(request):
    if request.user.is_superuser:
        return redirect(adminbase)
    if request.method=='GET':
        return render(request,'adminlogin.html')  
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['pass']
        user=authenticate(username=username,password=password)
        if user is not None and user:
            login(request, user)
            return redirect(dashboard)
        else:
            messages.error(request, 'wrong credentials enter valid details!!')
            return redirect(adminlogin)              
    return render(request,'adminlogin.html') 


def adminbase(request):
    if request.user.is_authenticated and  request.user.is_superuser :
        return render(request, 'dashboard.html')
    else:    
        return render(request , 'adminlogin.html')    


def logoutadmin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        logout(request)
    return redirect('adminlogin')


def userlist(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        if 'search' in request.GET:
            search = request.GET['search']
            multiple_search = Q(Q(first_name__icontains=search) | Q(username__icontains=search) | Q(email__icontains=search))
            ob = User.objects.filter(multiple_search)
        else:    
            ob=User.objects.all()
        return render(request,'userlist.html',{'ob':ob})
    else:        
         return redirect('adminlogin')  

def adminorder(request):
    if request.user.is_authenticated and request.user.is_superuser:
        ob = Myorders.objects.all().order_by('-id')
        context={'ob':ob}
        return render(request,'adminorder.html', context)
    else:
        return redirect(adminlogin)

def cancelorderr(request,id):
    if request.user.is_authenticated and  request.user.is_superuser:
        obj = Myorders.objects.values('status','orderstatus').get(id=id)
        if obj['orderstatus'] == 'Placed':
            if obj['status']==True:
                try:
                    Myorders.objects.filter(id=id).update(status=False)
                except:
                    pass
                n='order cancelled'
                messages.info(request,n)
                return redirect(adminorder)
            else:
                return redirect(adminorder)
        else:
            return redirect(adminorder)
    else:
         return redirect(adminlogin)
            



def orderstatus(request,id):
    if request.user.is_authenticated and  request.user.is_superuser:
        ob = Myorders.objects.values('orderstatus','status').get(id=id)
        if ob['status']==True:
            if ob['orderstatus']=='Placed':
                Myorders.objects.filter(id=id).update(orderstatus='shipped')
                n= 'Status updated successfully to Shipped'
                messages.success(request,n)
                return redirect(adminorder)
            if ob['orderstatus']=='shipped':
                Myorders.objects.filter(id=id).update(orderstatus='Out For delivery')
                n= 'Status updated successfully to Out for delivery'
                messages.success(request,n)
                return redirect(adminorder)
            if ob['orderstatus']=='Return Pending':
                Myorders.objects.filter(id=id).update(orderstatus='RETURN INTIATED')
                n= 'Status updated successfully to RETURN INTIATED'
                messages.success(request,n)
                return redirect(adminorder)
            if ob['orderstatus']=='Out For delivery':
                Myorders.objects.filter(id=id).update(orderstatus='deliverd')
                n= 'Status updated successfully to Delivered'
                messages.success(request,n)
            else:
               return render(request,'adminorder.html')
        else:
            return redirect(adminorder)   
    else:
        return redirect(adminorder)             

@never_cache
def dashboard(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        product = Stock.objects.all()
        bb = Myorders.objects.all()
        revenue = 0
        for i in bb:
            revenue = revenue + int(i.amount)                       #type:ignore

        use = Stock.objects.count()
        ob = Myorders.objects.filter(orderstatus='deliverd').count()
        pending = Myorders.objects.filter(orderstatus='Placed').count() 
           
        
        order   = Myorders.objects.all()
        context={'product':product,'use':use,'ob':ob,'bb':bb,'pending':pending,'revenue':revenue}

        product = Stock.objects.all()
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=365))
        yearly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        mmax = timezone.now()
        mmin = (timezone.now() - datetime.timedelta(days=30))
        monthly = Myorders.objects.filter(orderdate__lte=mmax, orderdate__gte=mmin)
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=7))
        weekly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        a = []
        n = 1
        subm = timezone.now()
        n = 4
        for i in range(4):
            k = 0
            for i in monthly:
                if i.orderdate <= subm and i.orderdate >= (subm - datetime.timedelta(days=7)):      #type: ignore
                    k += 1

            a.append({'name': 'week' + str(n), 'value': k})
            n -= 1
            subm = subm - datetime.timedelta(days=7)

        subw = timezone.now()
        n = 7
        b = []
        for i in range(7):
            k = 0
            for i in weekly:
                if i.orderdate <= subw and i.orderdate >= (subw - datetime.timedelta(days=1)):      #type: ignore
                    k += 1
            b.append({'name': 'day' + str(n), 'value': k})
            n -= 1
            subw = subw - datetime.timedelta(days=1)
        monthly_sales = list(reversed(a))
        weekly_sales = list(reversed(b))
        user_count = User.objects.all().count()
        order_price = Payment.objects.all().aggregate(Sum('totalamount'))
        total_income = order_price['totalamount__sum']
        order_count = Myorders.objects.all().count()
        product_count = product.count()
        payment = Payment.objects.all()

        obje = Myorders.objects.filter(orderdate__year=2022)
        
        obje1 = Myorders.objects.values('orderdate','orderid','amount','orderstatus').annotate(month=TruncMonth('orderdate')).values('month','orderdate','orderid','amount','orderstatus').annotate(c=Count('id')).values('month','c','orderdate','orderid','amount','orderstatus')
        
        lol=[]
        for i in obje1:
            lol.append({'order_id':i['orderid'],'delivery_status':i['orderstatus'],'month':i['month'].month,'year':i['month'].year,'total_price':i['amount']})
            
        return render(request, 'dashboard.html',
                    context={'monthly': monthly, 'yearly': yearly, 'monthly_sales': monthly_sales,
                            'weekly_sales': weekly_sales, 'user_count': user_count, 'total_income': total_income,
                            'order_count': order_count, 'product_count': product_count, 'payment': payment, 'lol':lol,'revenue':revenue,'product':product,'use':use,'ob':ob,'bb':bb,'pending':pending, })
    else:
        return redirect(adminlogin)    
        
     

def sales_report(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        product = Stock.objects.all()
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=365))
        yearly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        mmax = timezone.now()
        mmin = (timezone.now() - datetime.timedelta(days=30))
        monthly = Myorders.objects.filter(orderdate__lte=mmax, orderdate__gte=mmin)
        ymax = timezone.now()
        ymin = (timezone.now() - datetime.timedelta(days=7))
        weekly = Myorders.objects.filter(orderdate__lte=ymax, orderdate__gte=ymin)
        a = []
        n = 1
        subm = timezone.now()
        n = 4
        for i in range(4):
            k = 0
            for i in monthly:
                if i.orderdate <= subm and i.orderdate >= (subm - datetime.timedelta(days=7)):  # type: ignore
                    k += 1

            a.append({'name': 'week' + str(n), 'value': k})
            n -= 1
            subm = subm - datetime.timedelta(days=7)

        subw = timezone.now()
        n = 7
        b = []
        for i in range(7):
            k = 0
            for i in weekly:
                if i.orderdate <= subw and i.orderdate >= (subw - datetime.timedelta(days=1)):    # type: ignore
                    k += 1
            b.append({'name': 'day' + str(n), 'value': k})
            n -= 1
            subw = subw - datetime.timedelta(days=1)
        monthly_sales = list(reversed(a))
        weekly_sales = list(reversed(b))
        user_count = User.objects.all().count()
        order_price = Payment.objects.all().aggregate(Sum('totalamount'))
        total_income = order_price['totalamount__sum']
        order_count = Myorders.objects.all().count()
        product_count = product.count()
        payment = Payment.objects.all()

        obje = Myorders.objects.filter(orderdate__year=2022)
        obje1 = Myorders.objects.values('orderdate','orderid','amount','orderstatus').annotate(month=TruncMonth('orderdate')).values('month','orderdate','orderid','amount','orderstatus').annotate(c=Count('id')).values('month','c','orderdate','orderid','amount','orderstatus')

        lol=[]
        for i in obje1:
            lol.append({'orderid':i['orderid'],'orderdate':i['orderdate'].date,'orderstatus':i['orderstatus'],'month':i['month'].month,'year':i['month'].year,'totalamount':i['amount']})
        return render(request, 'report.html',
                      context={'monthly': monthly,'yearly': yearly, 'monthly_sales': monthly_sales,
                               'weekly_sales': weekly_sales, 'user_count': user_count, 'total_income': total_income,
                               'order_count': order_count,'product_count': product_count,'payment':payment,'lol':lol})
    else:
        return redirect(adminlogin)   
    
    
    
def date_wise(request):
    if request.method=="POST":
        start = request.POST['start_date']
        end = request.POST['end_date']
        if len(start)<1:
            messages.error(request,"choose correct Date")
            return redirect(sales_report)
        if len(end)<1:
           messages.error(request,"choose correct Date")
           return redirect(sales_report)
        order = Myorders.objects.filter(orderdate__range=[start,end])
        o_count =len(order)
        return render(request, 'report.html',{'lol':order,'o_count':o_count})
    else:
        return render(request, 'report.html')   
    
    
def coupon_management(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            name         = request.POST['name']
            couponcode   = request.POST['couponcode']
            validdate    = request.POST['validdate']
            minimumprice = request.POST['minimumprice']
            discount     = request.POST['discount']
            ins = Coupon(coupon_name = name,coupon_code=couponcode,validtill=validdate,minimum_price=minimumprice,discount=discount)
            ins.save()
            n = ' Coupon is  added SuccessFully '
            messages.success(request,n)
            return redirect(coupon_management)

        coupon = Coupon.objects.all()
        context ={'coupon':coupon} 
        return render(request,'coupon.html',context) 
    else:
        return redirect(adminlogin)    
    
def delete_coupon(request,id):
    co = Coupon.objects.filter(id=id)
    co.delete()
    Coupon.objects.all()
    n = ' Coupon Deleted Successfully'
    messages.success(request,n)
    return redirect(coupon_management)                        
            


    





   