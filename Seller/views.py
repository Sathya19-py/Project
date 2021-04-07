from django.contrib import messages
from django.shortcuts import render, redirect

from Farmer.models import Order
from .models import Seller_Registration, Product
import datetime


# Create your views here.


def S_Valid(request):
    Email = request.POST.get('email')
    Password = request.POST.get('password')

    try:
        Seller_Registration.objects.get(Email_Id=Email, Password=Password)
        request.session['Seller_Email'] = Email
        # request.session.set_expiry(30)
        return render(request, 'Seller/S_Home.html')
    except:
        return redirect('slogin')


def S_Login(request):
    try:
        if request.session['Seller_Email']:
            return redirect('shome')
        else:
            return render(request, 'Seller/dlogin.html')
    except KeyError:
        return render(request, 'Seller/dlogin.html')


def S_Registration(request):
    if request.method == "POST":
        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Mobile_Number = request.POST.get('mobile_number')
        Email_Id = request.POST.get('email_id')
        Shop_Name = request.POST.get('shop_name')
        Password1 = request.POST.get('password1')
        Password2 = request.POST.get('password2')

        if Seller_Registration.objects.filter(Email_Id=Email_Id).exists():
            messages.info(request, "Email Id Already Exists...Try with New One")
            return redirect('sreg')

        else:
            if Password1 == Password2:
                Seller_Registration(First_Name=First_Name, Last_Name=Last_Name, Mobile_Number=Mobile_Number,
                                    Email_Id=Email_Id, Shop_Name=Shop_Name, Password=Password1).save()
                return redirect('slogin')
            else:
                messages.info(request, "Passwords are Not Matching..Please check...")
                return redirect('sreg')

    else:
        return render(request, 'Seller/DRegistration.html')


def S_Home(request):
    try:
        if request.session['Seller_Email']:

            Email = request.session['Seller_Email']

            print('seller_email', Email)
            return render(request, 'Seller/S_Home.html')
        else:
            return render(request, 'Seller/dlogin.html')
    except KeyError:
        return render(request, 'Seller/dlogin.html')


def S_Add_Product(request):
    try:
        if request.session['Seller_Email']:

            Email = request.session['Seller_Email']

            print('seller_email', Email)
            return render(request, 'Seller/add_product.html')
        else:
            return render(request, 'Seller/dlogin.html')
    except KeyError:
        return render(request, 'Seller/dlogin.html')


def Add_Product(request):
    Product_Name = request.POST.get('product_name')
    Product_Price = request.POST.get('product_price')
    Product_Quantity = request.POST.get('product_quantity')
    Product_Weight = request.POST.get('product_weight')
    Product_Weight1 = request.POST.get('product_weight1')
    Product_Description = request.POST.get('product_description')
    Product_Image = request.FILES['product_image']
    Product_Status = request.POST.get('status')

    Add = Product(Product_Name=Product_Name, Product_Price=Product_Price, Product_Quantity=Product_Quantity,
                  Product_Weight=Product_Weight, Product_Weight1=Product_Weight1,
                  Product_Description=Product_Description,
                  Product_Image=Product_Image, Product_Status=Product_Status)
    Add.save()

    Email = request.session['Seller_Email']
    S_Data = Seller_Registration.objects.filter(Email_Id=Email).values('id')[0]['id']
    print("seller", S_Data)
    print("type", type(S_Data))

    sid = str(S_Data)
    print(sid)
    print("sid", sid)

    Add.Seller.set(sid)

    return redirect('s_add_pro')


def S_Products(request):
    try:
        if request.session['Seller_Email']:
            Email = request.session['Seller_Email']
            print('Email_id', Email)
            pro = Product.objects.filter(Seller__Email_Id=Email)
            print(pro)
            return render(request, 'Seller/stock.html', {'pro': pro})
        else:
            return render(request, 'Seller/dlogin.html')
    except KeyError:
        return render(request, 'Seller/dlogin.html')


def Update_Quantity(request):
    id = request.POST.get('id')
    option = request.POST.get('op')
    UQuan = int(request.POST.get('quantity'))
    if option == '+':
        res = Product.objects.filter(id=id)
        for x in res:
            Qua = x.Product_Quantity
            Product_Quantity = int(UQuan) + int(Qua)
            Product.objects.filter(id=id).update(Product_Quantity=Product_Quantity)
            return redirect('sproducts')
    else:
        res = Product.objects.filter(id=id)
        for x in res:
            Qua = x.Product_Quantity
            if UQuan <= Qua:
                Product_Quantity = int(Qua) - int(UQuan)
                Product.objects.filter(id=id).update(Product_Quantity=Product_Quantity)
                return redirect('sproducts')
            else:
                return redirect('sproducts')


def S_Update_Product(request):
    id = request.POST.get('id')
    pro = Product.objects.filter(id=id)
    return render(request, 'Seller/update_product.html', {'pro': pro})


def Change_Status(request):
    pid = request.POST.get('id')
    status = request.POST.get('status')

    if status == 'Active':
        Product.objects.filter(id=pid).update(Product_Status="InActive")
        return redirect('sproducts')
    else:
        Product.objects.filter(id=pid).update(Product_Status="Active")
        return redirect('sproducts')


def Update_Product(request):
    id = request.POST.get('id')

    Product_Name = request.POST.get('product_name')
    Product_Price = request.POST.get('product_price')
    Product_Quantity = request.POST.get('product_quantity')
    Product_Weight = request.POST.get('product_weight')
    Product_Weight1 = request.POST.get('product_weight1')
    Product_Description = request.POST.get('product_description')
    Product_Image = request.FILES.get('product_image')
    Product_Status = request.POST.get('status')

    print(Product_Image)

    if Product_Image == None:
        Product.objects.filter(id=id).update(Product_Name=Product_Name, Product_Price=Product_Price,
                                             Product_Quantity=Product_Quantity, Product_Weight=Product_Weight,
                                             Product_Weight1=Product_Weight1, Product_Description=Product_Description,
                                             Product_Status=Product_Status)

        return redirect('sproducts')

    else:
        print('with image')
        pro = Product.objects.get(id=id)
        print(pro)
        pro.Product_Name = Product_Name
        pro.Product_Price = Product_Price
        pro.Product_Quantity = Product_Quantity
        pro.Product_Weight = Product_Weight
        pro.Product_Weight1 = Product_Weight1
        pro.Product_Description = Product_Description
        pro.Product_Status = Product_Status
        pro.Product_Image = Product_Image
        pro.save()
        return redirect('sproducts')


def S_Delete_Product(request):
    Did = request.POST.get('id')
    Product.objects.filter(id=Did).delete()
    return redirect('sproducts')


def S_Orders(request):
    try:
        if request.session['Seller_Email']:

            Email = request.session['Seller_Email']
            ord = Order.objects.filter(Seller__Email_Id=Email)

            print('seller_email', Email)
            return render(request, 'Seller/sorders.html',{'ord':ord})
        else:
            return render(request, 'Seller/dlogin.html')
    except KeyError:
        return render(request, 'Seller/dlogin.html')


def S_Update_Order(request):
    oid = request.POST.get('id')
    print(oid)
    ord = Order.objects.filter(Order_Id=oid)
    for x in ord:
        Expected = x.Order_Date
        print(Expected)
        Expected_Date = Expected + datetime.timedelta(days=7)
        print(Expected_Date)
    return render(request, 'Seller/sorder_details.html',{'ord':ord,'Expected_Date':Expected_Date})

def Cancel_Order(request):
    oid = request.POST.get('id')
    Status_Date = datetime.datetime.today()
    Order_Status = 'Order Cancelled'
    Order.objects.filter(Order_Id=oid).update(Order_Status=Order_Status, Status_Date=Status_Date)
    messages.info(request, 'order status is updated')
    return redirect('sorders')

def Update_Status(request):
    oid = request.POST.get('id')
    option = request.POST.get('option')
    print(oid)
    print(option)

    Status_Date = datetime.datetime.today()

    ord = Order.objects.filter(Order_Id=oid)
    for x in ord:
        Expected = x.Order_Date
        print(Expected)
        Expected_Date = Expected + datetime.timedelta(days=7)


    if option == 'select':
        messages.info(request, "Please select an option")
        return redirect('sorders')
        # return render(request, 'Seller/sorder_details.html',{'ord':ord,'Expected_Date':Expected_Date})
    elif option == 'Processing':
        Order.objects.filter(Order_Id=oid).update(Order_Status=option, Status_Date=Status_Date)
        messages.info(request, 'order status is updated')
        return redirect('sorders')
        # return render(request, 'Seller/sorder_details.html',{'ord':ord,'Expected_Date':Expected_Date})
    elif option == 'Shipped':
        Order.objects.filter(Order_Id=oid).update(Order_Status=option, Status_Date=Status_Date)
        messages.info(request, 'order status is updated')
        return redirect('sorders')
        # return render(request, 'Seller/sorder_details.html', {'ord': ord, 'Expected_Date': Expected_Date})
    elif option == 'Delivered':
        Order.objects.filter(Order_Id=oid).update(Order_Status=option, Status_Date=Status_Date)
        messages.info(request, 'order status is updated')
        return redirect('sorders')
        # return render(request, 'Seller/sorder_details.html', {'ord': ord, 'Expected_Date': Expected_Date})
    else:
        for x in ord:
            status = x.Order_Status
            if status == 'Order Placed':
                Expected_Date = Expected + datetime.timedelta(days=7)
                return redirect('sorders')
                # return render(request, 'Seller/sorder_details.html', {'ord': ord, 'Expected_Date': Expected_Date})




def S_Profile(request):
    try:
        if request.session['Seller_Email']:

            Email = request.session['Seller_Email']

            sel = Seller_Registration.objects.filter(Email_Id=Email)
            return render(request, 'Seller/sprofile.html', {'sel': sel})
        else:
            return render(request, 'Seller/dlogin.html')
    except KeyError:
        return render(request, 'Seller/dlogin.html')


def S_Edit_Profile(request):
    try:
        if request.session['Seller_Email']:
            sid = request.GET['id']
            sel = Seller_Registration.objects.filter(id=sid)
            return render(request, 'Seller/sprofile_edit.html', {'sel': sel})
        else:
            return render(request, 'Seller/dlogin.html')
    except KeyError:
        return render(request, 'Seller/dlogin.html')



def Update_Profile(request):
    sid = request.POST.get('id')

    First_Name = request.POST.get('first_name')
    Last_Name = request.POST.get('last_name')
    Mobile_Number = request.POST.get('mobile_number')
    Email_Id = request.POST.get('email_id')
    Shop_Name = request.POST.get('shop_name')
    Password = request.POST.get('password')


    S_Email = request.session['Seller_Email']

    if S_Email == Email_Id:
        Seller_Registration.objects.filter(id=sid).update(First_Name=First_Name, Last_Name=Last_Name,
                                                          Mobile_Number=Mobile_Number,
                                                          Shop_Name=Shop_Name, Password=Password)
        return redirect('sprofile')
    else:
        if Seller_Registration.objects.filter(Email_Id=Email_Id).exists():
            messages.info(request, "Email Id Already Exists...Try with New One")
            return redirect('sprofile')

        else:
            Seller_Registration.objects.filter(id=sid).update(First_Name=First_Name, Last_Name=Last_Name,
                                                              Mobile_Number=Mobile_Number, Email_Id=Email_Id,
                                                              Shop_Name=Shop_Name, Password=Password)
            request.session['Seller_Email'] = Email_Id

            return redirect('sprofile')



def S_Logout(request):
    try:
        del request.session['Seller_Email']
        return redirect('slogin')
    except KeyError:
        return redirect('slogin')
