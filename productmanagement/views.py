
from django.contrib import messages
from cartmanagement.models import Guestcart
from django.shortcuts import render,redirect
from cartmanagement.models import Cart
from productmanagement.models import Banner, Stock
from gameadmin.models import User,Categories
# Create your views here.


def product(request):
    p=Stock.objects.all()
    return render(request , 'product.html',{'p':p})


def addproducts(request):
    ob=Categories.objects.all()

    if request.method=='POST':
        name = request.POST['name']
        categor =request.POST['category']
        price  = request.POST['price']
        stock = request.POST['stock']
        quantity = request.POST['quantity']
        description = request.POST['description']
        filename1 = request.FILES.get('filename1')
        filename2 = request.FILES.get('filename2')
        filename3 = request.FILES.get('filename3')
        filename4 = request.FILES.get('filename4')
        
        ins = Stock(name=name, price= price,stock=stock, quantity=quantity,category_id=categor, description=description,image1=filename1,image2=filename2,image3=filename3,image4=filename4)
        
        ins.save()
        return redirect(product)
    return render(request, 'addproducts.html',{'ob':ob})


def editproducts(request,id):
    if request.user.is_authenticated:

        oj  = Categories.objects.all()
        n = 'Edit Product'
        pro  = Stock.objects.get(id = id)
        context={'oj':oj,  'n':n,'pro':pro}
        
        
        if request.method=='POST':
            pro         = Stock.objects.get(id = id)
            name        = request.POST['name']
            category    = request.POST['category'] 
            price       = request.POST['price']
            stock       = request.POST['stock']
            quantity    = request.POST['quantity']
            description = request.POST['description']
            pro.name        = name
            pro.price       = price
            pro.stock       = stock
            pro.quantity    = quantity
            pro.description = description
            pro.save()
            n ='Product Updated'
            return redirect(product)
        return render(request, 'editproduct.html',context)
    else:
        return redirect("/")

def delete_user(request,id):
    o = Stock.objects.get(id=id)
    o.delete()
    n = 'Product Removed'
    Stock.objects.all()
    return redirect(product)   


def categories(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        if request.method=='POST':
            name=request.POST['categories']
            offer = request.POST['offer']
            if Categories.objects.filter(name=name).exists():
                messages.warning(request,' Named category already found')
                return redirect(categories)
            else:
                category = Categories(name=name,offer=offer)
                category.save()
                messages.success(request,'category Added')
                return redirect(categories)
    cat = Categories.objects.all()
    context = {'cat':cat }
    return render(request, 'categories.html',context)

def delete_categories(request,id):
    ob=Categories.objects.get(id=id)
    ob.delete()
    return redirect('categories')     

def product_details(request,id):
    ob = Stock.objects.all().get(id=id)
    count = Stock.objects.all().filter(id=id).count()
    related_products = Stock.objects.filter(category=ob.category).exclude(id=id)[:4]
    p = Stock.objects.all()
    cat = Categories.objects.values('offer').get(id=ob.category_id)                 #type:ignore
    pro = ob.proOffer
    c =cat['offer']
    if c >= pro: 
        offeredprice = ob.price - (ob.price * cat['offer'])/100
        request.session['offer'] = offeredprice
    else:
        offeredprice = ob.price - (ob.price * pro)/100
        request.session['offer'] = offeredprice

    context = {'ob':ob,'c':c,'offeredprice':offeredprice,'count':count ,'pro':pro,'p':p, 'related_products':related_products}
    if request.method == 'POST':
        quantity = request.POST['quantity']
        request.session['quantity']=quantity
        if request.user.is_authenticated and request.user.is_active:
            ca= Cart.objects.filter(userid=request.user).count()

            p =  Stock.objects.all().get(id=id)
            u = User.objects.all().get(id=request.user.id)
            
            if Cart.objects.filter(productid=id,userid=request.user).exists():
                c = Cart.objects.get(productid_id=id,userid=request.user)
                c.productname = p.name
                c.productid = p
                c.userid= u
                c.quantity=c.quantity + int(quantity)
                c.image = p.image1      # type: ignore
                c.amount=c.amount*int(quantity)
                c.save()
                n = 'Added to Cart'
                messages.info(request,n)
                
            else:
                offer = request.session['offer']
                t = Cart(productname = p.name, productid= p,userid = u,price=p.price,quantity= quantity,image=p.image1)
                if int(quantity)>1:
                    t.amount=p.price*int(quantity)

                else:
                    t.amount = offer
                t.save()
                n = 'Added to Cart'
                messages.info(request,n)
        else:
            quantity = request.session['quantity']
            
            if not request.session.session_key:
                request.session.create()
            request.session['guest_key']=request.session.session_key
            key = request.session['guest_key']
            offer =request.session['offer']
            p =  Stock.objects.all().get(id=id)
            if Guestcart.objects.filter(productid_id=id,userreference=key).exists():
                g = Guestcart.objects.get(productid_id=id,userreference=key)
                
                g.quantity = g.quantity + int(quantity)
                g.save()
                n = 'Added to Cart'
                messages.info(request,n)
            else:
                t = Guestcart(productname = p.name,userreference=key, productid= p,price=p.price,quantity= quantity,image=p.image1)
                if int(quantity)>1:
                    t.amount=p.price*int(quantity)
                else:
                    t.amount = p.price
                t.save()
                n = 'Added to Cart'
                messages.info(request,n)
    return render(request,'productdetails.html',context)

def filter(request,id):
    cat = Categories.objects.all()
    cate = Categories.objects.get(id=id)
    u = Stock.objects.filter(category=id)
    users=[]
    for i in u:
        users.append({
             "id"  : i.id,  # type: ignore
            "name"  : i.name,
            "price" : i.price,
            "quantity" : i.quantity,
            "stock"  : i.stock,
            "description":i.description,
            "image1"    : i.image1,
            "image2"    : i.image2,
            "image3"    : i.image3,
            "image4"    : i.image4,
            "proOffer"  : i.proOffer,
            "offeredprice" :i.price -  i.price * (i.proOffer/100)
        }) 
    context = {'p':users,'cat':cat,'cate':cate}
    return render(request, 'viewhome.html',context)

def offer_management(request):
    cat = Categories.objects.all().order_by('id')
    product = Stock.objects.all().order_by('id')
    context = {'cat':cat,'product':product}
    return render(request,'offer.html',context)

def edit_offer(request,id):
    if request.method=='POST':
        offer = request.POST['offer']
        Categories.objects.filter(id=id).update(offer=offer)
        n="offer updated"
        messages.warning(request,n)
        return redirect(offer_management)
    return render(request,'editoffer.html')

def edit_proOffer(request,id):
    if request.method == 'POST':
        offer = request.POST['offer']
        Stock.objects.filter(id=id).update(proOffer=offer)
        messages.info(request,'Product offer updated')
        return redirect(offer_management)
    return render(request,'editoffer.html')

def banner(request):
    if request.user.is_authenticated:
        ban = Banner.objects.all()
        return render(request, 'banner.html',{'ban':ban})
    else:
        return redirect("/")
    
def add_banner(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=='POST':
            heading = request.POST['heading']
            filename= request.FILES.get('filename')
            description = request.POST['description']
            ins = Banner(heading=heading,image=filename,description=description)
            ins.save()
            n = 'Banner is Added'
            messages.warning(request,n)
            return redirect(banner)
        return render(request,'addBanner.html')
    else:
        return redirect("/")    

def delete_banner(request,id):
    ban = Banner.objects.get(id=id)
    ban.delete()
    n = 'Banner Deleted Successfully'
    messages.info(request,n)
    return redirect(banner)

  



    