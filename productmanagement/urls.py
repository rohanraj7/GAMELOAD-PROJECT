from django.urls import path,include
from . import views
urlpatterns = [
    path('productmanagement/',views.product,name='product'),
    path('addproducts/',views.addproducts,name='addproducts'),
    path('editproduct/<int:id>/',views.editproducts,name='editproducts'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('categories/', views.categories, name='categories'),
    path('deletecategories/ <id>',views.delete_categories,name='delete_categories'),
    path('products/ <id>',views.product_details,name='product_details'),
    path('filter/ <id>',views.filter,name='filter'),
    path('offermanagement/',views.offer_management,name='offer_management'),
    path('editoffer/ <id> ',views.edit_offer,name='edit_offer'),
    path('edit_proOffer/ <id>',views.edit_proOffer,name='edit_proOffer'),
    path('banner/',views.banner,name='banner'),
    path('addBanner/',views.add_banner, name='add_banner'),
    path('deleteBanner/ <id>',views.delete_banner,name='delete_banner'),
]