from django.urls import path
from Seller import views

urlpatterns = [
    path('slogin/',views.S_Login,name="slogin"),
    path('svalid/',views.S_Valid,name="svalid"),
    path('sreg/',views.S_Registration,name="sreg"),
    path('shome/',views.S_Home,name='shome'),

    path('s_add_pro/', views.S_Add_Product, name='s_add_pro'),
    path('add_pro/',views.Add_Product,name='add_pro'),

    path('sproducts/', views.S_Products, name='sproducts'),
    path('add_quantity/',views.Update_Quantity,name='add_quantity'),
    path('update/',views.Update_Product,name='update'),
    path('s_update_product/', views.S_Update_Product, name='s_update_product'),
    path('s_delete_product/',views.S_Delete_Product,name='s_delete_product'),
    path('change_status/',views.Change_Status,name='change_status'),

    path('sorders/', views.S_Orders, name='sorders'),
    path('s_update_order/', views.S_Update_Order, name='s_update_order'),
    path('cancel_order/', views.Cancel_Order, name='cancel_order'),
    path('update_status/',views.Update_Status,name='update_status'),


    path('sprofile/', views.S_Profile, name='sprofile'),
    path('edit_profile/',views.S_Edit_Profile,name='edit_profile'),
    path('update_profile/',views.Update_Profile,name='update_profile'),

    path('slogout/',views.S_Logout,name="slogout")

]