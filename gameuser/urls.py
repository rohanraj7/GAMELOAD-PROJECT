from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('viewhome/',views.view_home,name='view_home'),
    path('login/', views.login_view,name='login_view'),
    path('logoutuser/', views.logout_user, name='logout_user'),
    path('signup/', views.signup,name='signup'),
    path('otp/', views.otp,name='otp'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/',views.edit_profile,name='edit_profile'),
    path('address/',views.address,name='address'),
    path('changepassword/',views.change_password,name='change_password'),
    path('deleteaddress/<id>',views.delete_address,name='delete_address'),
    path('numbercheck/',views.number_check,name='number_check'),
    path('otpvalidate/',views.otp_validate,name='otp_validate'),

]