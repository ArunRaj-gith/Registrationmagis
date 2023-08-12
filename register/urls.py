from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('profile',views.profile,name='profile'),
    path('forgotpass',views.Forgot_password,name='forgotpass'),
    path('createpro',views.CreateProfile,name='createpro'),
    path('editpro',views.EditProfile,name='editpro'),
    path('propic',views.upload_image,name='propic'),
    path('changepass',views.Change_password,name='changepass'),
    path('verifypass',views.reset_password,name='verifypass'),
]