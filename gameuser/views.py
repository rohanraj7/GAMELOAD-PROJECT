from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from twilio.rest import Client
from cartmanagement.models import Cart
from gameuser.mixins import MessageHandler
from gameadmin.models import Address, User,Categories
from gameload import verify
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from productmanagement.models import Banner, Stock


# Create your views here.

def home(request):
    return render(request , 'home.html')


@never_cache  
def login_view(request):
    if request.user.is_authenticated:
        return redirect(view_home)
    if request.method == 'POST':
        email = request.POST['email'] 
        password = request.POST['password']
        user = authenticate(email=email,password=password)
     

        if user is not None:
            login(request, user)
            n= 'login Successfuly'
            messages.success(request,n)  
            return redirect(view_home)
        else:
            n = 'invalid credentials'
            messages.success(request,n)
            return redirect(login_view)
    return render(request, 'login.html')    


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        n = 'Logout Successfully'
        messages.info(request,n)
    return redirect(login_view) 
  

@never_cache
def view_home(request):      
    if request.user.is_authenticated:
         user=User.objects.all().get(id=request.user.id)
         ban =  Banner.objects.values()
         p=Stock.objects.all()
         products=[]
         for i in p:
             products.append({
                 "id"    : i.id,                              # type: ignore
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
         paginator = Paginator(products,5)
         page_number = request.GET.get('page')
         productdata = paginator.get_page(page_number)
         totalpage = productdata.paginator.num_pages
         cat = Categories.objects.all()
         name= request.GET.get('search')
         
         
# ____________SEARCH________

         if request.method == 'GET' and name is not None:
             ban = Banner.objects.values()
             match = Stock.objects.values('name','price','quantity','image1','description','id','stock').annotate(search=SearchVector('name','description')).filter(search=name)
             c = Cart.objects.filter(userid=request.user).count()
             return render(request , 'viewhome.html',{'match': match,'cat':cat,'c':c,'ban':ban})
         context= {'p':productdata,'lastpage':totalpage,'cat':cat,'user':user,'ban':ban,'list':[n+1 for n in range(totalpage)]} 
         return render(request,'viewhome.html',context) 

#______________GUEST USER____________
    
    else:
        p = Stock.objects.all()    
        ban = Banner.objects.values() 
        products = []
        for i in p:
            products.append({
                "id"    : i.id,  # type: ignore
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
        paginator = Paginator(products,5)
        page_number = request.GET.get('page')
        productdata = paginator.get_page(page_number)
        totalpage = productdata.paginator.num_pages
        cat = Categories.objects.all()
        name= request.GET.get('search')
        print("kjnj")
        print(name)
         
# ____________SEARCH________

        if request.method == 'GET' and name is not None:
            match = Stock.objects.values('name','price','quantity','image1','description','id','stock').annotate(search=SearchVector('name','description')).filter(search=name)
            # c = Cart.objects.filter(userid=request.user).count()
            return render(request , 'viewhome.html',{'match': match,'cat':cat,'p':p})
        context= {'p':productdata,'lastpage':totalpage,'cat':cat,'ban':ban,'list':[n+1 for n in range(totalpage)]} 
        return render(request,'viewhome.html',context)     
    return redirect(login_view)     
        


def signup(request):
    if request.method =='POST':
        fullname = request.POST['name']
        email = request.POST['email']
        phoneno = request.POST['phone_no']
        password1 = request.POST['password']
        password2 = request.POST['password1']
        
        if password1!=password2:
            messages.error(request,('password did no match'))
            return redirect(signup)

        if fullname.isspace():
            messages.error(request,('Name should not contain spaces'))
            return redirect(signup)

        if email.isspace():
            messages.error(request,('username should not contain spaces'))
            return redirect(signup)
        if User.objects.filter(phoneno=phoneno).exists():
            messages.info(request,'phone no already taken')
            return redirect(signup)

        if User.objects.filter(email=email).exists():
            messages.info(request,'email taken')
            return redirect(signup)
        else:
            request.session['phoneno']=phoneno
            phone=phoneno
            verify.send(phone)
            user = User.objects.create_user( fullname=fullname,phoneno=phoneno ,email=email, password=password1)
            user.save()
            return redirect(otp)
    return render(request, 'signup.html')



def otp(request):
    if request.user.is_authenticated:
        return redirect('view_home')
    if request.method =='POST':
        phoneno=request.session['phoneno']
        code = request.POST.get('code')
        k=verify.checked(phone=phoneno,code=code)  
        # verify.check()                                                   
        if k:
            User.objects.filter(phoneno=phoneno).update(active=True)
            return redirect(view_home)
        else:
            return redirect(number_check)
    return render(request,'otpverify.html')   

def number_check(request):
    if request.user.is_authenticated:
        return redirect('view_home')
    if request.method=='POST':
        phone=request.POST['phoneno']
        verify.send(phone) 
        return redirect(otp_validate)
    return render(request,'otp.html')

def otp_validate(request):
    if request.user.is_authenticated:
        return redirect('login_home')
    if request.method=='POST':
        phone=request.POST['phone']
        otp1= int(request.POST['code'])
        validate = verify.checked(phone=phone,code=otp1)  
        if validate=="approved":
            messages.error(request, 'login success')
            return render(request,'view_home.html')
        else:
             messages.error(request, 'Wrong Credentials')
             return render(request,'otpverify.html')
    return render(request,'otpverify.html')
           

    

def profile(request):
    if request.user.is_authenticated:
        ob=User.objects.all().get(id=request.user.id)
        o =Address.objects.filter(user_id=request.user)
        context={'ob':ob,'o':o}
        return render(request,'myprofile.html',context)
    return redirect(login_view)

def edit_profile(request):
    ob = User.objects.filter(id=request.user.id)
    if request.method=='POST':
        name        = request.POST['name']
        if name.isspace():
            messages.error(request,('Name should not contain spaces'))
            return redirect(edit_profile)
        if  name.isnumeric():
            messages.error(request,('Name should not contain Numbers'))
            return redirect(edit_profile)

        User.objects.filter(id=request.user.id).update(fullname=name)
        return redirect(profile)

    return render(request,'editprofile.html')

def address(request):
    if request.method=='POST':
        housename=request.POST['housename']
        city     =request.POST['city']
        district =request.POST['district']
        zipcode  =request.POST['zipcode']
        if housename.isspace():
            messages.error(request,('Housename should not contain spaces'))
            return redirect(address)
        if housename.isnumeric():
                messages.error(request,('Housename should not contain Numbers'))
                return redirect(address)
        if city.isspace():
            messages.error(request,('Cityname should not contain spaces'))
            return redirect(address)
        if housename.isnumeric():
            messages.error(request,('City should not contain Numbers'))
            return redirect(address)
        if district.isspace():
            messages.error(request,('Districtname should not contain spaces'))
            return redirect(address)
        if  district.isnumeric():
            messages.error(request,('District should not contain Numbers'))
            return redirect(address)
        if zipcode.isspace():
            messages.error(request,('Name should not contain spaces'))
            return redirect(address)
        else:

            ins = Address(user=request.user,housename=housename, city1=city, district1=district, zipcode1=zipcode )
            ins.save()
            return redirect(profile)
    return render(request,'address.html')

def change_password(request):
    if request.user.is_authenticated:
         if request.method=='POST':
            password1    = request.POST['password1']
            newpassword1 = request.POST['newpassword1']
            newpassword2 = request.POST['newpassword2']
            if newpassword1.isspace():
                messages.error(request,('Password should not contain spaces'))
                return redirect(change_password)
            
            o = check_password(password1,request.user.password)            
            if o:
                if newpassword1 == newpassword2:
                    user = User.objects.get(id=request.user.id)
                    user.set_password(newpassword1)
                    user.save()

                    messages.success(request,('password changed'))
                    return redirect(change_password)
                else:
                    messages.error(request,('password did not match'))
                    return redirect(change_password)
            else:
                messages.error(request,('old password is wrong'))
                return redirect(change_password)

    else:
        return redirect("/")  
    return render(request,'password.html')

def delete_address(request,id):
    dele = Address.objects.filter(id=id)
    dele.delete()

    return redirect(profile)    
    