from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
import uuid
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
from django.http import HttpResponse
from django.views import View
import requests
import json
from django.db.models import Q
from django.contrib.auth.models import User as UserModel
from django.core.mail import EmailMultiAlternatives
from django.template import loader

# Create your views here.
def base(request):
    return render(request, 'Smart_Parking_App/basic_files/base.html' )

def whyus(request):
    return render(request, 'Smart_Parking_App/basic_files/why.html' )

def about(request):
    return render(request, 'Smart_Parking_App/basic_files/about.html' )

def parkhome(request):
    return render(request, 'Smart_Parking_App/basic_files/parkhome.html' )

def contact(request):
     if request.method == 'POST':
       name = request.POST.get('name')
       message = request.POST.get('message')
       email = request.POST.get('email')
       phone = request.POST.get('phone')

      

       context={
           'name' : name,
           'message' : message,
           'email' : email,
           'phone' : phone,
       }

       

       email=EmailMultiAlternatives(
           "You got Promotions", message,
           '',
           ['zunairsaleem06@gmail.com'] 
       )
       email.send()
       messages.success(request, 'Your Request Successfully Submit. We will contact you Soon!')
     return render(request, 'Smart_Parking_App/basic_files/contact.html' )

def home(request):

    return render(request, 'Smart_Parking_App/basic_files/home.html' )

# Registration Process
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not username.isalnum():
            messages.error(request, 'Username must be alphanumeric')
            return redirect('signup')
        
        try:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken.')
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is taken.')
                return redirect('signup')

            user_obj = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)


            send_mail_after_registration(email, auth_token)

            return redirect('token_send')

        except Exception as e:

            messages.error(request, 'An error occurred while processing your request.')
            print(e)

    return render(request, 'Smart_Parking_App/basic_files/signup.html')

def success(request):
    return render(request , 'Smart_Parking_App/basic_files/success.html')


def token_send(request):
    return render(request , 'Smart_Parking_App/basic_files/token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()


        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')
    
def error_page(request):
    return  render(request , 'Smart_Parking_App/basic_files/error.html')

def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

# Login Process
def login_user(request):
  
  if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login')
        
        login(request , user)

        return redirect('home')
  
  return render(request, 'Smart_Parking_App/basic_files/login.html')

def logout_user(request):
    logout(request)
    return redirect('parkhome')

@login_required(login_url="login")
def garage(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/'+ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)


    return  render(request , 'Smart_Parking_App/garage/garage.html',{'data' : location_data})

@login_required(login_url="login")
def garage_home(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/'+ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)
    return  render(request , 'Smart_Parking_App/garage/garagehome.html', {'data' : location_data})

@login_required(login_url="login")
def garage_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
         form = ProfileForm(request.POST, request.FILES, instance=request.user.profile_edit)
         if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, your Profile is Updated.')
            return redirect('garagehome')
         else:
             pass
    return  render(request , 'Smart_Parking_App/garage/profile.html', {'form':form})

# //chat_Puropse_demo_views
@login_required(login_url="login")
def chat_home(request):
    User = get_user_model()
    users = User.objects.all()
    chats = {}
    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        chats = chatMessages.objects.filter(Q(user_from=request.user.id, user_to=request.GET['u']) | Q(user_from=request.GET['u'], user_to=request.user.id))
        chats = chats.order_by('date_created')
    context = {
        "page":"index",
        "users":users,
        "chats":chats,
        "chat_id": int(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    }
    print(request.GET['u'] if request.method == 'GET' and 'u' in request.GET else 0)
    return render(request,"Smart_Parking_App/garage/index.html",context)

@login_required(login_url="login")
def get_messages(request):
    chats = chatMessages.objects.filter(Q(id__gt=request.POST['last_id']),Q(user_from=request.user.id, user_to=request.POST['chat_id']) | Q(user_from=request.POST['chat_id'], user_to=request.user.id))
    new_msgs = []
    for chat in list(chats):
        data = {}
        data['id'] = chat.id
        data['user_from'] = chat.user_from.id
        data['user_to'] = chat.user_to.id
        data['message'] = chat.message
        data['date_created'] = chat.date_created.strftime("%b-%d-%Y %H:%M")
        print(data)
        new_msgs.append(data)
    return HttpResponse(json.dumps(new_msgs), content_type="application/json")

@login_required(login_url="login")
def send_chat(request):
    resp = {}
    User = get_user_model()
    if request.method == 'POST':
        post =request.POST
        
        u_from = UserModel.objects.get(id=post['user_from'])
        u_to = UserModel.objects.get(id=post['user_to'])
        insert = chatMessages(user_from=u_from,user_to=u_to,message=post['message'])
        try:
            insert.save()
            resp['status'] = 'success'
        except Exception as ex:
            resp['status'] = 'failed'
            resp['mesg'] = ex
    else:
        resp['status'] = 'failed'

    return HttpResponse(json.dumps(resp), content_type="application/json")
#End chat Views

#POST Related Views
@login_required(login_url="login")
def post_index(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/'+ip_data["ip"])
    location_data_one = res.text
    location_data = json.loads(location_data_one)
    query = request.GET.get("q")
    if query:
        products=Product.objects.filter(Q(name__icontains=query))
    else:
        products = Product.objects.all()
        # context = {"products": products}
    return render(request, 'Smart_Parking_App/garage/post.html', {"products": products,'data' : location_data})

@login_required(login_url="login")
def detail(request, id):
    product = Product.objects.get(id=id)
    images = Image.objects.filter(product=product)
    context = {"product": product, "images": images}
    return render(request, 'Smart_Parking_App/garage/detail_page.html', context)
    
@login_required(login_url="login")
def create_product(request):
    productform = ProductForm()
    imageform = ImageForm()
    
    if request.method == 'POST':
        
        files = request.FILES.getlist('images')
        
        productform = ProductForm(request.POST, request.FILES)
        if productform.is_valid():
            product = productform.save(commit=False)
            product.vendor = request.user
            product.save()
            messages.success(request, "Product created successfully")
            
            for file in files:
                Image.objects.create(product=product, images=file)
            
            return redirect("post")
    
    context = {"p_form": productform, "i_form": imageform}
    return render(request, 'Smart_Parking_App/garage/uploadpost.html', context)

@login_required(login_url="login")
def myadd(request):
    products = Product.objects.filter(vendor=request.user)
    context = {"products": products}
    return render(request, 'Smart_Parking_App/garage/myadd.html', context)

@login_required(login_url="login")
def search(request):
    query = request.GET.get("booking")
    if query:
        booking=parking_detail.objects.filter(Q(parking_area__icontains=query))
    else:
        booking = parking_detail.objects.all()
        # context = {"products": products}
    return render(request, 'Smart_Parking_App/parking/search.html', {"booking": booking})



# for generating pdf invoice
@login_required(login_url="login")
def reserve_parking(request,pk):
    print(pk)
    park = parking_detail.objects.get(pk=pk)
    if request.method == 'POST':
        owner_name=request.POST.get('owner_name')
        vehicle_name=request.POST.get('vehicle_name')
        vehicle_no=request.POST.get('vehicle_no')
        vehicle_brand=request.POST.get('vehicle_brand')
        vehicle_color=request.POST.get('vehicle_color')
        vehicle_model=request.POST.get('vehicle_model')
        parking_time=request.POST.get('parking_time')
        phone=request.POST.get('phone')
        cnic_no=request.POST.get('cnic_no')
        license_no=request.POST.get('license_no')
        
        reserve_parking=reserve(owner_name=owner_name, vehicle_name=vehicle_name, vehicle_brand=vehicle_brand, vehicle_no=vehicle_no, vehicle_color=vehicle_color, vehicle_model=vehicle_model, parking_time=parking_time,phone=phone,cnic_no=cnic_no,license_no=license_no)
        reserve_parking.save()

        pn = park.location
        dis = park.parking_area
        charges = park.charges
        booking = reserve.objects.all()
        total_amount=charges*parking_time
        data={'plocation':pn, 'area':dis,'name':owner_name, 'vname':vehicle_name, 'vno':vehicle_no, 'vb':vehicle_brand, 'vc':vehicle_color,'vm':vehicle_model,'pt':parking_time,'ph':phone,'amount':total_amount, "c":charges,"cnic":cnic_no,"license":license_no}
        return render(request, 'Smart_Parking_App/parking/pdf.html',{'data': data, 'booking': booking})
    
    return render(request, 'Smart_Parking_App/parking/parkbase.html')

@login_required(login_url="login")
def pdf(request):
    booking = reserve.objects.all()
    return render(request,'Smart_Parking_App/parking/pdf.html',{'booking':booking})

def navbar(request):
    return render(request, 'Smart_Parking_App/garage/navbar.html')