from django.urls import path
from Farmer import views

urlpatterns = [
    path('',views.Index,name="index"),
    path('mpro/',views.Main_Products,name="mpro"),


    path('flogin/',views.F_Login,name="flogin"),
    path('f_valid/',views.F_Valid,name='f_valid'),

    path('freg/',views.F_Registration,name="freg"),
    path('contact_us/',views.Contact_Us,name="contact_us"),

    path('fhome/',views.F_Home,name="fhome"),
    path('fpro/',views.F_Products,name="fpro"),

    path('fcart/',views.F_Cart,name="fcart"),
    path('add_cart/',views.Add_Cart,name='add_cart'),
    path('update_cart/',views.Update_Cart,name='update_cart'),
    path('delete_cart/',views.Delete_Cart,name='delete_cart'),

    path('forders/',views.F_Orders,name="forders"),
    path('order_details/',views.Order_details,name='order_details'),


    path('fprofile/',views.F_Profile,name="fprofile"),
    path('check_out/',views.Check_Out,name="check_out"),
    path('place_order/',views.Place_Order,name='place_order'),

    path('f_edit_profile/',views.F_Profile_Edit,name="f_edit_profile"),
    path('fupdate_profile/',views.FUpdate_Profile,name='fupdate_profile'),

    path('f_address/',views.F_Address,name="f_address"),
    path('add_address/',views.Add_Address,name='add_address'),
    path('edit_address/',views.Edit_Address,name='edit_address'),
    path('update_address/',views.Update_Address,name='update_address'),
    path('delete_address/',views.Delete_Address,name='delete_address'),

    path('flogout',views.F_Logout,name='flogout'),


]