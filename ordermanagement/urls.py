from django.urls import path,include
from . import views
urlpatterns = [
        path('checkout/',views.checkout,name='checkout'),
        path('myorder/ ',views.myorder,name='myorder'),
        path('cancelorder/ <id>',views.cancel_order,name='cancelorder'),
        path('success_cash/',views.success_cash,name='success_cash'),
        path('success/',views.success,name='success'),
        path('return/ <id>',views.return_item,name="return_item"),
        

        
]