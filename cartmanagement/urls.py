from django.urls import path,include
from . import views

urlpatterns = [
        path('cartview/',views.view_cart,name='view_cart'),
        path('removecart/ <id>',views.remove_cart,name='remove_cart'),
        path('dquantity/',views.dquantity,name='dquantity'),
        path('iquantity/',views.iquantity,name="iquantity"),
        path('addwishlist/<id>',views.add_wishlist,name='add_wishlist'),
        path('viewwishlist/',views.view_wishlist,name='view_wishlist'),
        path('removewishlist/<id>',views.remove_wishlist,name='remove_wishlist'),
]