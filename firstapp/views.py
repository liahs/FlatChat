from django.shortcuts import render, get_object_or_404,reverse,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from firstapp.models import contact_us,signup_model,category,add_property,booked
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from firstapp.forms import add_property_form
from django.db.models import Q
from django.core.mail import EmailMessage
from datetime import datetime
import requests
import random
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal

def home(request):
    context = {}
    all_property = add_property.objects.all().order_by("property_name")
    check = signup_model.objects.filter(user__id=request.user.id)
    print(check)
    if len(check)>0:
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
   
    cats = category.objects.all()
    context["category"] = cats
    context['prop']=all_property
    return render(request,"home.html",context)

def signin(request):
    return render(request,"signin.html")

def aboutus(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"aboutus.html",context)

def category_type(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    cats = category.objects.all()
    context ["category"] = cats
    return render(request,"category.html",context)

def contact(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        msg = request.POST["message"]
        nm = request.POST["name"]
        em = request.POST["email"]
        sub = request.POST["subject"]

        data = contact_us(message=msg,name=nm,email=em,subject=sub)
        data.save()
        res = "Dear {} thanks for your feedback".format(nm)
        return render(request,"contact.html",{"status": res})

    return render(request,"contact.html",context)

def signup(request):
    if "user_id" in request.COOKIES:
        uid = request.COOKIES["user_id"]
        usr = get_object_or_404(User,id=uid)
        login(request,usr)
        if usr.is_superuser:     
         return HttpResponseRedirect("/admin")

        if usr.is_active:     
         return HttpResponseRedirect("/customer_dashboard")
    if request.method=="POST":
        fname = request.POST["first"]
        last = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        con = request.POST["contact"]
        tp = request.POST["utype"]
        # print(request.POST)

        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = last

        if tp == "sell":
            usr.is_staff = True
        usr.save()

        sig = signup_model(user=usr,contact_number=con)
        sig.save()
        return render(request,"signup.html",{"status": "Mr./Mrs {} your account created successfully".format(fname)})
    return render(request,"signup.html")

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def user_login(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["pwd"]
        
        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                res=HttpResponseRedirect("/admin")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now())
                return res
            else:
                res = HttpResponseRedirect("/customer_dashboard")
                if "rememberme" in request.POST:
                    res.set_cookie("user_id",user.id)
                    res.set_cookie("date_login",datetime.now())

                return res
            # if user.is_active:
            #     return HttpResponseRedirect("/customer_dashboard")
        else:
            return render(request,"home.html",{"status":"Invaid Username"})
        
    return HttpResponse("Called")

def edit_profile(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        # print(request.FILES)
        fn = request.POST["fname"]
        ln = request.POST["lname"]
        em = request.POST["email"]
        con = request.POST["contact"]
        age = request.POST["age"]
        gen = request.POST["gender"]
        ct = request.POST["city"]
        occ = request.POST["occ"]
        abt = request.POST["about"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        data.contact_number = con
        data.age = age
        data.city = ct
        data.occupation = occ
        data.gender = gen
        data.about = abt
        data.save()

        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_picture = img
            data.save()

        context["status"] = "Changes Saved Successfully"
    return render(request,"edit_profile.html",context)

def change_password(request):
    context = {}
    ch = signup_model.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        
        if check==True:
            user.set_password(new_pas)
            user.save()
            user = User.objects.get(username=un)
            login(request,user)
            context["msz"] = "Password Change successfully"
            context["col"] = "alert-success"
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)

@login_required
def customer_dashboard(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"customer_dashboard.html",context)

@login_required
def seller_dashboard(request):
    return render(request,"seller_dashboard.html")

@login_required
def user_logout(request):
    logout(request)
    res =  HttpResponseRedirect("/")
    res.delete_cookie("user_id")
    res.delete_cookie("date_login")
    return res

def property_detail(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:

        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    id = request.GET["pid"]
    obj = add_property.objects.get(id=id)
    context["property"] = obj
    
    #paypal
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(obj.booking_amount/70),
        'item_name': obj.property_name,
        'invoice': str(id),
        'notify_url': 'http://{}{}'.format('127.0.0.1:8000',redirect('paypal-ipn')),
        'return_url': 'http://{}{}'.format('127.0.0.1:8000',
                                           reverse('payment_done',kwargs={'pid':id})),
        'cancel_return': 'http://{}{}'.format('127.0.0.1:8000',
                                            redirect('payment_cancelled')),
    }
    
    print(redirect('paypal-ipn').url)
    form = PayPalPaymentsForm(initial=paypal_dict)
    context["form"]=form
    return render(request,"property_detail.html",context)


def payment_done(request,pid):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    obj = add_property.objects.get(id=pid)
    obj.property_status='Sold'
    obj.save()
    b=booked(buyer=context['data'],prop=obj)
    b.save()
    return HttpResponseRedirect('/books')


def payment_cancelled(request):
    print(request)
    return HttpResponseRedirect('')


def properties(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"property.html",context)

def add_property_view(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if check[0].user.is_staff:
        if len(check)>0:
            data = signup_model.objects.get(user__id=request.user.id)
            context["data"] = data
            form = add_property_form()
            print()
            if request.method=="POST":
                form = add_property_form(request.POST,request.FILES)
                if form.is_valid():
                    data = form.save(commit=False)
                    login_user = User.objects.get(username=request.user.username)
                    data.seller = login_user
                    data.save()
                    context["status"] = "{} Added successfully".format(data.property_name)
            context["form"] = form
        
        return render(request,"add_property.html",context)
    else:
        return HttpResponse("<H1>Only Staff can access</H1>")

def my_property(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    all = add_property.objects.filter(seller__id=request.user.id)
    context["property"] = all
    return render(request,"my_property.html",context)

def single_property(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
        
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data

    id = request.GET["pid"]
    obj = add_property.objects.get(id=id)
    context["property"] = obj
    return render(request,"single_property.html",context)

def update_property(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    cats = category.objects.all()
    context["category"] = cats

    pid = request.GET["pid"]
    properties = add_property.objects.get(id=pid)
    context["property"] = properties

    if request.method=="POST":
        pn = request.POST["pname"]
        ct_id = request.POST["pcat"]
        pr = request.POST["pp"]
        sp = request.POST["sp"]
        ba = request.POST["bamt"]
        cty = request.POST["city"]
        ps = request.POST["pstatus"]
        area = request.POST["parea"]
        bath = request.POST["bath"]
        bed = request.POST["pbed"]
        bal = request.POST["bal"]
        des = request.POST["des"]

        cat_obj = category.objects.get(id=ct_id)

        properties.property_name = pn
        properties.property_category = cat_obj
        properties.property_price = pr
        properties.sale_price = sp
        properties.booking_amount = ba
        properties.city = cty
        properties.property_status = ps
        properties.area = area
        properties.no_of_bathroom = bath 
        properties.no_of_bedroom = bed
        properties.Balconies = bal
        properties.details = des
        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            properties.property_images = img

        if "pimg2" in request.FILES:
            img2 = request.FILES["pimg2"]
            properties.image1 = img2

        if "pimg3" in request.FILES:
            img3 = request.FILES["pimg3"]
            properties.image2 = img3

        if "pimg4" in request.FILES:
            img4 = request.FILES["pimg4"]
            properties.image3 = img4

        properties.save()
        context["status"] = "Changes Saved Successfully!!!"
        context["id"] = pid
    return render(request,"update_property.html",context)

def delete_property(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
      
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data

    if "pid" in request.GET:
        pid = request.GET["pid"]
        prd = get_object_or_404(add_property, id=pid)
        context["property"] = prd
        if "action" in request.GET:
            prd.delete()
            context["status"] = str(prd.property_name)+ "removed Successfully!!!"
    return render(request,"delete_property.html",context)

def all_property(request):
    context = {}
    all_property = add_property.objects.all().order_by("property_name")
    context["property"] = all_property
    cats = category.objects.all()
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    context["category"] = cats
    if "qry" in request.GET:
        q = request.GET["qry"]
        c = request.GET["cty"]
        prd = add_property.objects.filter(Q(property_name__icontains=q)|Q(property_category__cat_name__contains=q)|Q(city=c))
        context["property"] = prd
        context["abcd"] = "Search"
    if "cat" in request.GET:
        cid = request.GET["cat"]
        prd = add_property.objects.filter(property_category__id=cid)
        context["property"] = prd
        context["abcd"] = "Search"
    return render(request,"all_property.html",context)

def sendemail(request):
    context = {}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = signup_model.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        # print(request.POST)
        rec = request.POST["to"].split(",")
        # print(rec)
        sub = request.POST["sub"]
        msz = request.POST["msz"]
        try:
            em = EmailMessage(sub,msz,to=rec)
            em.send()
            context["status"] = "Email Sent"
            context["cls"] = "alert-success"
        except:
            context["status"] = "Could not sent, please check your internet connection / Email Address"
            context["cls"] = "alert-danger"
    return render(request,"sendemail.html",context)

def forgotpass(request):
    context = {}
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()

        login(request,user)
        if user.is_superuser:
            return HttpResponseRedirect("/admin")
        else:
            return HttpResponseRedirect("/customer_dashboard")
        # context["status"] = "Password Change Successfully!!!"

    return render(request,"forgot_password.html",context)

def resetpass(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "Dear {} \n {} is your one time password (OTP) dont not share with others \n Thanks & Regards \n RealEstate".format(user.username,otp)
        try:
            email = EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status": "sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status": "error","email":user.email})

    except:
        return JsonResponse({"status":"failed"})
    

def books(request):
    context={}
    check = signup_model.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = signup_model.objects.get(user__id=request.user.id)
        context['data']=data
    b=booked.objects.get(buyer=context['data']) if booked.objects.filter(buyer=context['data']) else 0
    context['b']=b
    return render(request,'booked.html',context)

# def process_payment(request):
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#     host = request.get_host()
 
#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': '100',
#         'item_name': 'house',
#         'invoice': '1',
#         'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
#     }
 
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     return render(request, '', {'order': order, 'form': form})
