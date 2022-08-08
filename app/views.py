from django.http.request import validate_host
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer, OrderPlaced, Product, Cart
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, password_validation
from django.views import View
from .forms import CustomerProfileForm, CustomerAdrsForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.utils.translation import gettext_lazy as _

global val
def val(prodlist):
    prods = []
    for prod in prodlist:
        temp = []
        mrp = prod.mrp
        sp = prod.selling_price
        off = ((mrp-sp)*100)//mrp
        temp.append(prod)
        temp.append(int(off))
        prods.append(temp)
    return prods


def home(request):
    prodlist = Product.objects.all()
    prods = []
    for prod in prodlist:
        mrp = prod.mrp
        sp = prod.selling_price
        off = ((mrp-sp)*100)//mrp
        if off > 20:
            prods.append(prod)

    return render(request, 'app/home.html', {'prods':prods})

# def product_detail(request):

#     return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk = pk)
        status = False
        if Cart.objects.filter(pk=pk).exists():
            status = True
        else:
            status = False
        return render(request, 'app/productdetail.html', {'product':product, 'status':status})
 

@login_required(login_url="login")
def add_to_cart(request):
    if request.method == "POST":
        user = request.user
        product_id = request.POST.get('prod_id')
        print(product_id)
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
    return redirect('/cart')

@login_required(login_url="login")
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        usercart = Cart.objects.filter(user=user)
        if len(usercart) == 0:
            return render(request, 'app/emptycart.html')
        else:
            amt = 0
            for prod in usercart:
                amt = amt + (prod.product.selling_price*prod.quant)
            tax = (amt*18)/100
            total = amt + tax
            if total < 500:
                total = total + 60
            else:
                total = total + 0
            return render(request, 'app/addtocart.html', {'carts':usercart, 'amt':amt, 'tax':tax, 'total': round(total,2)})


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quant += 1
        c.save()
        amt = 0
        usercart = Cart.objects.filter(user=request.user)
        for prod in usercart:
            amt = amt + (prod.product.selling_price*prod.quant)
        tax = (amt*18)/100
        total = amt + tax
        if total < 500:
            total = total + 60
        else:
            total = total + 0
        data = {
            'quant':c.quant,
            'amount':amt,
            'tax':tax,
            'total':round(total,2),
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        if c.quant > 1:
            c.quant -= 1
            c.save()
            amt = 0
            usercart = Cart.objects.filter(user=request.user)
            for prod in usercart:
                amt = amt + (prod.product.selling_price*prod.quant)
            tax = (amt*18)/100
            total = amt + tax
            if total < 500:
                total = total + 60
            else:
                total = total + 0
            data = {
                'quant':c.quant,
                'amount':amt,
                'tax':tax,
                'total':round(total,2),
            }
            return JsonResponse(data)

@login_required(login_url="login")
def remove_item(request):
     if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        data = {}
        return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

@method_decorator(login_required(login_url="login"), name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            # usr = request.user
            # name = form.cleaned_data['name']
            # addres = form.cleaned_data['addres']
            # city = form.cleaned_data['city']
            # pincode = form.cleaned_data['pincode']
            # state = form.cleaned_data['state']
            # prof = Customer(user=usr, name=name, addres=addres, city=city, pincode=pincode, state=state)
            # prof.save()
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profile details updated succesfully !')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})





@login_required(login_url="login")        
def address(request):
    Alladrs = Customer.objects.filter(user = request.user)
    return render(request, 'app/address.html', {'alladrs':Alladrs, 'active':'btn-primary'})

@login_required(login_url="login")
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orders':op})


def grocery(request):
    allprods = Product.objects.filter(category='groc') 
    prods = val(allprods)
    return render(request, 'app/electronic.html', {'prods':prods})
 

def dailyess(request):
    allprods = Product.objects.filter(category='dailyess') 
    prods = val(allprods)
    return render(request, 'app/electronic.html', {'prods':prods})

def fruits(request):
    fruitsprods = Product.objects.filter(category='fr_vegie')
    fruits = val(fruitsprods)
    return render(request, 'app/fruits.html', {'fruits':fruits})

def frozen(request):
    allprods = Product.objects.filter(category='frozen') 
    prods = val(allprods)
    return render(request, 'app/frozen.html', {'prods':prods})

def homecare(request):
    allprods = Product.objects.filter(category='homecare') 
    prods = val(allprods)
    return render(request, 'app/homecare.html', {'prods':prods})


def bedbath(request):
    allprods = Product.objects.filter(category='bedbath') 
    prods = val(allprods)
    return render(request, 'app/bedbath.html', {'prods':prods})

def electronic(request):
    allprods = Product.objects.filter(category='electronics') 
    prods = val(allprods)
    return render(request, 'app/electronic.html', {'prods':prods})

def footwears(request):
    allprods = Product.objects.filter(category='footwears') 
    prods = val(allprods)
    return render(request, 'app/electronic.html', {'prods':prods})

def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = email.split('@')[0]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Log in succesfull !')
            return redirect('/')

        else:
            messages.warning(request, 'INVALID CREDENTIALS !')
            return redirect('login')

    return render(request, 'app/login.html')

@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    messages.success(request, 'User has been Logged out succesfully !')
    return redirect('/')

def change_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email == request.user.email:
            user = User.objects.get(email=email)
            new_pass = request.POST.get('password1')
            confirm_pass = request.POST.get('password2')
            if(new_pass == confirm_pass):
                user.set_password(new_pass)
                user.save()
                messages.success(request, 'Password changed succesfully !')
            else:
                messages.warning(request, 'confirm password and new password field should be same !')
                return redirect('changepassword')
        else:
            messages.warning(request, 'Email doesnt match !')
            return redirect('changepassword') 

    return render(request, 'app/changepassword.html')
# class changepassword(PasswordChangeForm):
#     old_password = forms.CharField(label=_("Old Password"), strip=False, widget= forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))

#     new_password1 = forms.CharField(label=_("New Password"), strip=False, widget= forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html)

#     new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget= forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}))



def customerregistration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        username = email.split('@')[0]
        if User.objects.filter(username = username).exists():
            messages.warning(request, 'Email already taken !')
            return redirect('customerregistration')
        
        elif pass1 == pass2:
            user = User.objects.create_user(username=username, email=email, password=pass2)
            user.save()
            messages.success(request, 'User has been registered succesfully !')
            return redirect('login')

    return render(request, 'app/customerregistration.html')
 

def search(request):
    if request.method == "POST":
        query = request.POST.get('query')
        allprods = Product.objects.filter(title__icontains = query)
        fruits = []
        for prod in allprods:
            temp = []
            mrp = prod.mrp
            sp = prod.selling_price
            off = ((mrp-sp)*100)//mrp
            temp.append(prod)
            temp.append(int(off))
            fruits.append(temp)
        return render(request, 'app/search_res.html', {'fruits':fruits})

@login_required(login_url="login")
def checkout(request):
    user = request.user
    customr = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amt = 0
    for prod in cart_items:
        amt = amt + (prod.product.selling_price*prod.quant)
        tax = (amt*18)/100
        total = amt + tax
        if total < 500:
            total = total + 60
        else:
            total = total + 0
    return render(request, 'app/checkout.html', {'customers':customr, 'cart_items':cart_items, 'total': round(total,2), 'totalitems':len(cart_items)})

@login_required(login_url="login")
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product = c.product, quantity=c.quant).save()
        c.delete()
    return redirect("orders")
