from django.contrib import messages
from django.shortcuts import render,redirect
import datetime
import random
import string

from Seller.models import Product, Seller_Registration
from  .models import *

# Create your views here.

def Index(request):
    if Product.objects.all().exists():
        pro = Product.objects.all()
        return render(request,'index.html',{'pro':pro})
    else:
        d = True
        messages.info(request,"Products Are Not Available")
        return render(request, 'index.html',{'d':d})

def Main_Products(request):
    if Product.objects.all().exists():
        pro = Product.objects.all()
        return render(request,'Products.html',{'pro':pro})
    else:
        d = True
        messages.info(request, "Products Are Not Available")
        return render(request, 'Products.html', {'d': d})




def F_Valid(request):
    Email = request.POST.get('email')
    Password = request.POST.get('password')

    try:
        Farmer_Registration.objects.get(Email_Id=Email, Password=Password)
        request.session['Farmer_Email'] = Email
        # request.session.set_expiry(30)
        return render(request, 'Farmer/F_Home.html')
    except:
        return redirect('flogin')

def F_Login(request):
    try:
        if request.session['Farmer_Email']:
            return redirect('fhome')
        else:
            return render(request, 'Farmer/flogin.html')
    except KeyError:
        return render(request, 'Farmer/flogin.html')

def F_Registration(request):
    if request.method == "POST":
        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Mobile_Number = request.POST.get('mobile_number')
        Email_Id = request.POST.get('email_id')
        Password1 = request.POST.get('password1')
        Password2 = request.POST.get('password2')


        if Farmer_Registration.objects.filter(Email_Id=Email_Id).exists():
            messages.info(request, "Email Id Already Exists...Try with New One")
            return redirect('freg')

        else:
            if Password1 == Password2:
                Farmer_Registration(First_Name=First_Name, Last_Name=Last_Name, Mobile_Number=Mobile_Number,
                                    Email_Id=Email_Id, Password=Password1).save()
                return redirect('flogin')
            else:
                messages.info(request, "Passwords are Not Matching..Please check...")
                return redirect('freg')

    else:
        return render(request,'Farmer/FRegistration.html')


def Contact_Us(request):
    if request.method == 'POST':
        First_Name = request.POST.get('first_name')
        Last_Name = request.POST.get('last_name')
        Mobile_Number = request.POST.get('number')
        Email_Id = request.POST.get('email')
        Message = request.POST.get('messege')
        Contact(First_Name=First_Name,Last_Name=Last_Name,Mobile_Number=Mobile_Number,
                Email_Id=Email_Id,Message=Message).save()
        messages.info(request,'Thank You For Your Response...We will ge Back to you Soon...')
        return redirect('contact_us')
    else:
        return render(request,'contact.html')

def F_Home(request):
    try:
        if request.session['Farmer_Email']:

            F_Email = request.session['Farmer_Email']

            print('Farmer_Email', F_Email)
            return render(request,'Farmer/F_Home.html')
        else:
            return render(request, 'Farmer/flogin.html')
    except KeyError:
        return render(request, 'Farmer/flogin.html')


def F_Products(request):
    try:
        if request.session['Farmer_Email']:
            pro = Product.objects.all()
            return render(request,'Farmer/F_Products.html',{'pro':pro})
        else:
            return render(request, 'Farmer/flogin.html')
    except KeyError:
        return render(request, 'Farmer/flogin.html')


def F_Cart(request):
    try:
        if request.session['Farmer_Email']:

            F_Email = request.session['Farmer_Email']
            if Cart.objects.filter(Farmer__Email_Id=F_Email).exists():
                car = Cart.objects.filter(Farmer__Email_Id=F_Email)
                Total = 0
                for x in car:
                    Total += x.Sub_Total
                return render(request,'Farmer/cart.html',{'car':car,'Total':Total})
            else:
                messages.info(request, 'Your Cart is Empty..Keep Shoping...')
                d = True
                return render(request, "Farmer/cart.html",{'d':d})
        else:
            return render(request, 'Farmer/flogin.html')
    except KeyError:
        return render(request, 'Farmer/flogin.html')

def Add_Cart(request):
    pid = request.POST.get('id')
    Quantity = request.POST.get('quantity')
    pro = Product.objects.get(id=pid)
    Sub_Total = int(pro.Product_Price) * int(Quantity)

    F_Email = request.session['Farmer_Email']
    F_Data = Farmer_Registration.objects.get(Email_Id=F_Email)
    print('Farmer',F_Data)
    fid = str(F_Data)

    P_Data = Product.objects.get(id = pid)

    Sell = Product.objects.filter(id=pid).values_list('Seller__id',flat=True)

    print(Sell)

    for sel in Sell:
        S_Data = Seller_Registration.objects.get(id=sel)


    print("sid", fid)


    if Cart.objects.filter(Farmer__Email_Id=F_Email,products__id=pid).exists():
        messages.info(request,'Product Already Exists in Cart...')
        return redirect('fpro')
    else:
        if Quantity >= '1':
            cart1 = Cart(Quantity=Quantity, Sub_Total=Sub_Total, Farmer=F_Data,Seller=S_Data,products=P_Data)
            cart1.save()
            return redirect('fpro')
        else:
            messages.info(request, 'please select valid quantity...')
            return redirect('fpro')

def Update_Cart(request):
    cid = request.POST.get('id')
    option = request.POST.get('op')
    Qua = request.POST.get('qua')

    res = Cart.objects.filter(id=cid)

    if Qua >= '1':
        if option == '+':
            for x in res:
                Quantity = int(x.Quantity)+int(Qua)
                Total = int(x.products.Product_Price)*int(Qua)
                Sub = x.Sub_Total + Total
                Cart.objects.filter(id=cid).update(Sub_Total = Sub,Quantity=Quantity)

                return redirect('fcart')

        else:
            for x in res:
                if x.Quantity > int(Qua):
                    print('valid')
                    Quantity = int(x.Quantity)-int(Qua)
                    Total = int(x.products.Product_Price)*int(Qua)
                    Sub = x.Sub_Total - Total
                    Cart.objects.filter(id=cid).update(Sub_Total = Sub,Quantity=Quantity)

                    return redirect('fcart')
                else:
                    messages.info(request, "please select valid quantity")
                    return redirect('fcart')
    else:
        messages.info(request,"please select valid quantity")
        return redirect('fcart')

def Delete_Cart(request):
    cid = request.POST.get('id')
    Cart.objects.filter(id=cid).delete()
    return redirect('fcart')

def F_Orders(request):
    try:
        if request.session['Farmer_Email']:

            F_Email = request.session['Farmer_Email']
            ord = Order.objects.filter(Farmer__Email_Id=F_Email)
            return render(request,'Farmer/F_Orders.html',{'ord':ord})
        else:
            return render(request, 'Farmer/flogin.html')
    except KeyError:
        return render(request, 'Farmer/flogin.html')

def Check_Out(request):
    F_Email = request.session['Farmer_Email']
    car = Cart.objects.filter(Farmer__Email_Id=F_Email)
    if Delivery_Address.objects.filter(Farmer__Email_Id=F_Email).exists():
        add = Delivery_Address.objects.filter(Farmer__Email_Id=F_Email)
        Total = 0
        for x in car:
            Total += x.Sub_Total
        return render(request,'Farmer/check.html',{'car':car,"Total":Total,'add':add})
    else:
        d = True
        messages.info(request, 'Please Add a Delivery Address...')
        Total = 0
        for x in car:
            Total += x.Sub_Total
        return render(request, 'Farmer/check.html', {'car': car, "Total": Total,'d':d})

def Place_Order(request):
    F_Email = request.session['Farmer_Email']
    Payment_Mode = request.POST.get('Payment')
    aid = request.POST.get('address')
    Address = Delivery_Address.objects.get(id=aid)
    print('Address',Address)
    print('Farmer_Email', F_Email)
    cid = Cart.objects.filter(Farmer__Email_Id=F_Email).values_list('id', flat=True)

    Order_Status = 'Order Placed'

    for x in cid:
        res = Cart.objects.filter(id=x)
        for y in res:
            Seller = Seller_Registration.objects.get(id=y.Seller_id)
            Farmer = Farmer_Registration.objects.get(id=y.Farmer_id)
            product = Product.objects.get(id=y.products_id)
            Sub_total = y.Sub_Total
            Quantity = y.Quantity

            def Oid():
                x = random.randrange(1000000000, 9999999999)
                print(x)
                i = "OD"
                n = str(i)
                r = (n + str(x))
                num = str(r)
                print(num)
                try:
                    order = Order.objects.get(Order_Id=num)
                    Oid()
                except Order.DoesNotExist:
                    return num

            Order_Id = Oid()

            Order_Date = datetime.datetime.today()
            # Order_Date = dt.strftime("%d-%m-%Y %H:%M:%S")
            print(Order_Date)

            Status_Date = datetime.datetime.today()
            print(Status_Date)

        Order(Order_Id=Order_Id,Farmer=Farmer, Seller=Seller, product=product,
              Quantity=Quantity,Sub_Total=Sub_total,Payment_Mode=Payment_Mode,
              Order_Status=Order_Status,Order_Date=Order_Date,Status_Date=Status_Date,Address=Address).save()

    Cart.objects.filter(Farmer__Email_Id=F_Email).delete()

    return redirect('forders')

def Order_details(request):
    oid = request.GET['id']
    ord = Order.objects.filter(Order_Id=oid)
    for x in ord:
        Expected = x.Order_Date
        Expected_Date = Expected + datetime.timedelta(days=7)
    return render(request,'Farmer/forder_details.html',{'ord':ord,'Expected_Date':Expected_Date})

def F_Profile(request):
    try:
        if request.session['Farmer_Email']:

            F_Email = request.session['Farmer_Email']

            far = Farmer_Registration.objects.filter(Email_Id=F_Email)
            add = Delivery_Address.objects.filter(Farmer__Email_Id=F_Email)
            return render(request,'Farmer/f_profile.html',{'far':far,'add':add})
        else:
            return render(request, 'Farmer/flogin.html')
    except KeyError:
        return render(request, 'Farmer/flogin.html')


def F_Profile_Edit(request):
    try:
        if request.session['Farmer_Email']:
            fid = request.GET['id']
            far = Farmer_Registration.objects.filter(id=fid)
            return render(request, 'Farmer/fprofile_edit.html', {'far': far})
        else:
            return render(request, 'Farmer/flogin.html')
    except KeyError:
        return render(request, 'Farmer/flogin.html')



def FUpdate_Profile(request):
    fid = request.POST.get('id')

    First_Name = request.POST.get('first_name')
    Last_Name = request.POST.get('last_name')
    Mobile_Number = request.POST.get('mobile_number')
    Email_Id = request.POST.get('email_id')
    Password = request.POST.get('password')

    F_Email = request.session['Farmer_Email']

    if F_Email == Email_Id:
        Farmer_Registration.objects.filter(id=fid).update(First_Name=First_Name, Last_Name=Last_Name,
                                                          Mobile_Number=Mobile_Number,Password=Password)

        return redirect('fprofile')
    else:
        if Farmer_Registration.objects.filter(Email_Id=Email_Id).exists():
            messages.info(request, "Email Id Already Exists...Try with New One")
            return redirect('fprofile')
        else:
            Farmer_Registration.objects.filter(id=fid).update(First_Name=First_Name, Last_Name=Last_Name,
                                                              Mobile_Number=Mobile_Number,Email_Id=Email_Id,
                                                              Password=Password)
            request.session['Farmer_Email'] = Email_Id

            return redirect('fprofile')


def F_Address(request):
    return render(request,'Farmer/add_address.html')

def Add_Address(request):
    F_Email = request.session['Farmer_Email']

    Farmer = Farmer_Registration.objects.get(Email_Id=F_Email)
    Locality_Area = request.POST.get('locality_area')
    Landmark = request.POST.get('landmark')
    City = request.POST.get('city')
    State = request.POST.get('state')
    Pin_Code = request.POST.get('pin_code')

    Delivery_Address(Farmer=Farmer,Locality_Area=Locality_Area,Landmark=Landmark,City=City,State=State,Pin_Code=Pin_Code).save()

    return redirect('fprofile')

def Edit_Address(request):
    Aid = request.GET['id']
    add = Delivery_Address.objects.filter(id=Aid)
    return render(request,'Farmer/edit_address.html',{'add':add})

def Update_Address(request):
    Aid = request.POST.get('id')
    Locality_Area = request.POST.get('locality_area')
    Landmark = request.POST.get('landmark')
    City = request.POST.get('city')
    State = request.POST.get('state')
    Pin_Code = request.POST.get('pin_code')

    Delivery_Address.objects.filter(id=Aid).update(Locality_Area=Locality_Area,Landmark=Landmark,City=City,State=State,Pin_Code=Pin_Code)

    return redirect('fprofile')

def Delete_Address(request):
    Aid = request.GET['id']
    Delivery_Address.objects.filter(id=Aid).delete()
    return redirect('fprofile')

def F_Logout(request):
    try:
        del request.session['Farmer_Email']
        return redirect('flogin')
    except KeyError:
        return redirect('flogin')