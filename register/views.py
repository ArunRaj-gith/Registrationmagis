from django.contrib.auth.hashers import check_password
import requests
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import Profile



# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect(register)
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect(register)
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                print('User Created')
        else:
            messages.info(request, 'Password Not Matched')
            return redirect(register)
        return redirect(login)
    else:
        return render(request,'register.html')


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(profile)
        else:
            messages.info(request,'Invalid Details')
            return redirect(login)
    else:
        return render(request,'login.html')

def profile(request):
    # return render(request, 'profile.html')
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = Profile.objects.get(user_id=current_user.id)
    return render(request, 'profile.html', {'data': data, "data1": data1})

def CreateProfile(requset):
    data = User.objects.get(id = requset.user.id)
    if requset.method == "POST":
        phone = requset.POST['phone']
        dob = requset.POST['dob']
        address = requset.POST['address']
        city = requset.POST['city']

        prof = Profile.objects.create(user_id = requset.user.id,phone=phone,DOB=dob,address=address,city=city)
        prof.save()
        return redirect(profile)
    return render(requset,'createpro.html',{"data":data})


def EditProfile(request):
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = Profile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['address']
        city = request.POST['city']

        User.objects.filter(id=current_user.id).update(first_name=first_name,last_name=last_name,email=email)
        Profile.objects.filter(user_id = current_user.id).update(phone=phone,DOB=dob,address=address,city=city)
        return redirect(profile)
    return render(request, 'editpro.html', {'data': data,'data1':data1})


def upload_image(request):
    if request.method == 'POST' and request.FILES['images']:
        upload = request.FILES['images']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        Profile.objects.filter(user_id=request.user.id).update(profile_pic=file_url)
        return redirect(profile)

    return render(request,'propic.html')

def Change_password(request):

    if request.method == 'POST':
        old_pass = request.POST['oldpass']
        new_pass = request.POST['newpass']
        cnf_pass = request.POST['cpass']
        data = check_password(old_pass,request.user.password )
        if data:
            if new_pass == cnf_pass:
                u = User.objects.get(username=request.user.username)
                u.set_password(new_pass)
                u.save()
                print("password change successfully")

            else:
                print('password is not matching')
                return redirect(Change_password)
        else:
            print('Enter the correct password')
            return redirect(Change_password)

    return render(request,'changepass.html')



def Forgot_password(request):
    if request.method == 'POST':

        mobile = request.POST['phone']
        userdata = Profile.objects.get(phone=mobile)   # registered mobile number of user
        if userdata:
            url = "http://2factor.in/API/V1/482e2bfc-3db4-11ed-9c12-0200cd936042/SMS/{}/AUTOGEN".format(str(mobile))

            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=payload, headers=headers)
            data = response.json()

            r = data['Details']
            request.session['Details'] = r
            request.session['phone'] = mobile
            if data['Status'] == 'Success':
                return redirect(reset_password)
        else:
            return redirect(Forgot_password)
    return render(request, 'forgot.html')

def reset_password(request):
    if request.method == 'POST':
        otp = request.POST['OTP']
        passwd = request.POST['passw']
        cpasswd = request.POST['cpassw']
        details = request.session.get('Details')
        api = 'https://2factor.in/API/V1/482e2bfc-3db4-11ed-9c12-0200cd936042/SMS/VERIFY/{}/{}'.format(details, otp)
        res = requests.get(api).json()
        print(res)
        phone = request.session.get('phone')
        if res['Status'] == 'Success':
            if passwd == cpasswd:
                userdata = Profile.objects.get(phone=phone)
                data = User.objects.get(id=userdata.user_id)
                u = User.objects.get(username = data.username)
                u.set_password(passwd)
                u.save()

                return redirect(login)
    return render(request,'verify.html')



def logout(request):
    auth.logout(request)
    return redirect(home)