from django.urls import path,include
from . import views

urlpatterns = [
    path('adminlogin/', views.adminlogin,name='adminlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logoutadmin',views.logoutadmin,name='logoutadmin'),
    path('adminbase/',views.adminbase,name='adminbase'),
    path('userlist', views.userlist, name='userlist'),
    path('adminorder/',views.adminorder,name='adminorder'),
    path('orderstatus/ <id>',views.orderstatus,name='orderstatus'),  # type: ignore
    path('cancelorderr/<id>',views.cancelorderr,name='cancelorderr'),
    path('salesreport/',views.sales_report,name='sales_report'),
    path('datewise/',views.date_wise,name='date_wise'),
    path('couponmanagement',views.coupon_management,name='coupon_management'),
    path('deletecoupon/ <id>',views.delete_coupon,name='delete_coupon'),
]