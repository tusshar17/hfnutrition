from django.http import HttpResponse
from django.shortcuts import render, redirect
from requests import request
from store.models import *
from django.views import View
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
import re

# ==== Home Page ====
def home(request):
    categories = Category.get_categories()
    brands = Brand.get_brands()
    products = Product.get_trending_products()
    data = {
        'title': 'Healthify Nutrition',
        'item_list': products,
        'categories': categories,
        'brands': brands,
    }

    images = Images.get_all_face_images()
    data['images'] = images

    return render(request, "index.html", data)
# -------------------------------------------------


# ==== Category Page ====
def product_category(request, productCategory, categoryName):
    products = Product.get_products_by_category(productCategory)
    data = {
        'title': (categoryName + " | Healthify Nutrition"),
        'category': categoryName,
        'item_list': products
    }

    images = Images.get_all_face_images()
    data['images'] = images
    return render(request, "category.html", data)
# -------------------------------------------------

# ==== Category Page Sorted ====
def product_category_sorted(request,productCategory, categoryName,sortBy):

    if sortBy == 'PriceLowestFirst':
        products = Product.get_products_by_category_sorted(productCategory, 'selling_price')
    elif sortBy == 'PriceHighestFirst':
        products = Product.get_products_by_category_sorted(productCategory, 'selling_price')[::-1]
    elif sortBy == 'LatestFirst':
        products = Product.get_products_by_category(productCategory)

    data = {
        'title': (categoryName + " | Healthify Nutrition"),
        'category': categoryName,
        'categoryID': productCategory,
        'item_list': products,
        'sortBy' : sortBy
    }

    images = Images.get_all_face_images()
    data['images'] = images

    return render(request, "category.html", data)
# -------------------------------------------------


# ==== Product Page ====
class Product_Page(View):
    

    def post(self, request, productid):
        
        # check if user is logged in
        if request.session.get('customer_email') or request.session.get('customer_phone'):
            user_logged_in = True
        else:
            user_logged_in = False

        # 
        if user_logged_in:
            if request.session.get('customer_email'):
                customer_email = request.session['customer_email']
                customer = Customer.get_customer_by_contact(customer_email)
            elif request.session.get('customer_phone'):
                customer_phone = request.session['customer_phone']
                customer = Customer.get_customer_by_contact(customer_phone)

            cart1 = Cart.get_cart_products(customer)

            is_product_in_cart = Cart.is_product_in_cart(customer, productid)
            
            if is_product_in_cart:
                # product is already in cart
                cart_product = Cart.get_particular_product(customer, productid)
                if request.POST.get('remove-item-from-cart'):
                    if cart_product.qty == 1:
                        cart_product.delete()
                    else:    
                        cart_product.qty = cart_product.qty - 1
                        cart_product.register()
                else:
                    cart_product.qty = cart_product.qty + 1
                    cart_product.register()
                

            else:
                #product is not in cart
                prouct_instance = Product.get_product_by_id(productid)[0]
                cart_product = Cart(user=customer, product = prouct_instance, qty=1)
                cart_product.register() 

        else:
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(productid)
                if quantity:
                    if request.POST.get('remove-item-from-cart'):
                        if quantity==1:
                            cart.pop(productid)
                        else:
                            cart[productid] = quantity-1
                    else:
                        cart[productid] = quantity+1
                else:
                    cart[productid] = 1
                    
            else:
                cart = {}
                cart[productid] = 1

            request.session['cart'] = cart

        
        return redirect('/product/'+productid)

    
    def get(self, request, productid):
        product = Product.get_product_by_id([productid])[0]
        brand = Brand.get_brand_by_id(product.brand_id)[0]
        variants = Product.get_variants(product.prod_name)
        imgs = Images.get_images_by_prod(productid)
        info_img = Images.get_info_img(productid)[0]
        
        data = {
            'title': product.prod_name + "| Healthify Nutrition",
            'product': product,
            'brand': brand,
            'variants': variants,
            'imgs': imgs,
            'info_img': info_img 
        }

        # check if user loggerd in
        if request.session.get('customer_email') or request.session.get('customer_phone'):
            user_logged_in = True
        else:
            user_logged_in = False

        if user_logged_in:
            if request.session.get('customer_email'):
                customer_email = request.session['customer_email']
                customer = Customer.get_customer_by_contact(customer_email)
            elif request.session.get('customer_phone'):
                customer_phone = request.session['customer_phone']
                customer = Customer.get_customer_by_contact(customer_phone)

            data['is_product_in_cart'] = Cart.is_product_in_cart(customer, productid)
          
            if data['is_product_in_cart']:
                data['cart_product'] = Cart.get_particular_product(customer, productid)
        
        else:
            if request.session.get('cart'):
                data['is_product_in_cart'] = str(productid) in request.session.get('cart').keys()

        return render(request, "product.html", data)
# -------------------------------------------------


# ==== Cart Page ====
class Cart_Page(View):

    def post(self, request):
        # check if user is logged in
        if request.session.get('customer_email') or request.session.get('customer_phone'):
            user_logged_in = True
        else:
            user_logged_in = False

        prod_id = request.POST.get("post-prod-id")
        print(prod_id)
        if user_logged_in:
            if request.session.get('customer_email'):
                customer_email = request.session['customer_email']
                customer = Customer.get_customer_by_contact(customer_email)
            elif request.session.get('customer_phone'):
                customer_phone = request.session['customer_phone']
                customer = Customer.get_customer_by_contact(customer_phone)
            
            cart_product = Cart.get_particular_product(customer, prod_id)

            if request.POST.get("remove-item-from-cart"):
                if cart_product.qty == 1:
                    cart_product.delete()
                else:    
                        cart_product.qty -= 1
                        cart_product.register()
            else:
                cart_product.qty+=1
                cart_product.register()

        else:
            cart = request.session.get('cart')
            if cart:
                quantity = cart.get(prod_id)
                if quantity:
                    if request.POST.get('remove-item-from-cart'):
                        if quantity==1:
                            cart.pop(prod_id)
                        else:
                            cart[prod_id] = quantity-1
                    else:
                        cart[prod_id] = quantity+1
                else:
                    cart[prod_id] = 1
                    
            else:
                cart = {}
                cart[prod_id] = 1

            request.session['cart'] = cart


        return redirect("/cart")

    def get(self, request):
        data = {
            'title': "My Cart | Healthify Nutrition",
            'is_cart_empty' : False
        }

        # check if user loggerd in
        if request.session.get('customer_email') or request.session.get('customer_phone'):
            user_logged_in = True
        else:
            user_logged_in = False

        if user_logged_in:
            if request.session.get('customer_email'):
                customer_email = request.session['customer_email']
                customer = Customer.get_customer_by_contact(customer_email)
            elif request.session.get('customer_phone'):
                customer_phone = request.session['customer_phone']
                customer = Customer.get_customer_by_contact(customer_phone)

        # get all the products from cart
        if user_logged_in:
            data['cart_products'] = Cart.get_cart_products(customer)
            cart_prod_ids = list(Cart.get_cart_products(customer).values_list("product", flat=True))
            data['number_of_prod_in_cart'] = 0
            for i in range(len(cart_prod_ids)):
                cart_prod_ids[i] = str(cart_prod_ids[i])
                data['number_of_prod_in_cart'] += Cart.get_particular_product(customer, cart_prod_ids[i]).qty
            
            if len(data['cart_products']) == 0:
                data['is_cart_empty'] = True
            
        else:
            if request.session.get('cart'):
                session_cart = request.session.get('cart')
                cart_prod_ids=list(session_cart.keys())
                data['number_of_prod_in_cart'] = 0
                for id in cart_prod_ids:
                    data['number_of_prod_in_cart'] += request.session.get('cart')[id]
                data['cart_products'] = Product.get_product_by_id(list(session_cart.keys()))
            else:
                data['is_cart_empty'] = True

        
        data['img'] = {}

        if not data['is_cart_empty']:
            for id in cart_prod_ids:
                data['img'][id] = Images.get_face_image(int(id)).img

        
        data['user_logged_in'] = user_logged_in
        return render(request, "cart.html", data)
# -------------------------------------------------


# ==== Check Out Page ====
class CheckOut(View):

    def post(self, request):

        if request.session.get('customer_email'):
                customer_email = request.session['customer_email']
                customer = Customer.get_customer_by_contact(customer_email)
        elif request.session.get('customer_phone'):
                customer_phone = request.session['customer_phone']
                customer = Customer.get_customer_by_contact(customer_phone)

        address1 = request.POST.get('address')
        pin1 = request.POST.get('pin')
        state1 = request.POST.get('state')
        district1 = request.POST.get('district')
        city1 = request.POST.get('city')
        print(address1, pin1, state1, district1, city1)
        is_address_same = None
        if Address_Book.is_address_exists(customer):
            registered_add = Address_Book.get_customer_address(customer)
            is_address_same = (registered_add.address == address1)\
                and (registered_add.pin == pin1)\
                and (registered_add.state == state1)\
                and (registered_add.district == district1)\
                and (registered_add.city == city1)
            
        if is_address_same:
            new_address = registered_add
            
        else:
            new_address = Address_Book(user = customer,
                                    address=address1,
                                    pin=pin1, state=state1, 
                                    district=district1, city=city1)
            new_address.save()


        # order total
        cart = Cart.get_cart_products(customer)
        total = 0
        for item in cart:
            total += item.product.selling_price * item.qty

        order_instance = Order(
            user = customer,
            address = new_address,
            order_total = total
        )

        order_instance.register()

        for item in cart:
            order_line_instance = Order_Line(
                order_id = order_instance,
                product = item.product,
                price = item.product.selling_price,
                qty = item.qty
            )
            order_line_instance.register()
        cart.delete()
        return redirect("/order-placed")

    @method_decorator(auth_middleware)
    def get(self, request):
        data = {
            'title': "Healthify Nutrition"
        }

        # check if user loggerd in
        if request.session.get('customer_email') or request.session.get('customer_phone'):
            user_logged_in = True
        else:
            user_logged_in = False

        if user_logged_in:
            if request.session.get('customer_email'):
                customer_email = request.session['customer_email']
                customer = Customer.get_customer_by_contact(customer_email)
            elif request.session.get('customer_phone'):
                customer_phone = request.session['customer_phone']
                customer = Customer.get_customer_by_contact(customer_phone)

            data['customer'] = customer
            if Address_Book.is_address_exists(customer):
                data['address'] = Address_Book.get_customer_address(customer)

        # get all the products from cart
        if user_logged_in:
            data['cart_products'] = Cart.get_cart_products(customer)
        else:
            if request.session.get('cart'):
                session_cart = request.session.get('cart')
                cart_prod_ids=list(session_cart.keys())
                data['cart_products'] = Product.get_product_by_id(list(session_cart.keys()))




        return render(request, "checkout.html", data)
# -------------------------------------------------


# ==== order placed successfully ====
def order_confirmed(request):
    data = {
        'title': "Healthify Nurition"
    }

    if request.session.get('customer_email'):
        customer_email = request.session['customer_email']
        customer = Customer.get_customer_by_contact(customer_email)
    elif request.session.get('customer_phone'):
        customer_phone = request.session['customer_phone']
        customer = Customer.get_customer_by_contact(customer_phone)

    data['customer'] = customer

    return render(request, "order-placed.html", data)
# -------------------------------------------------


# ==== My Orders ====
def my_orders(request):
    data = {
        'title': "Healthify Nutrition"
    }

    if request.session.get('customer_email'):
        customer_email = request.session['customer_email']
        customer = Customer.get_customer_by_contact(customer_email)
    elif request.session.get('customer_phone'):
        customer_phone = request.session['customer_phone']
        customer = Customer.get_customer_by_contact(customer_phone)

    data['customer'] = customer

    data['orders'] = Order.get_customer_orders(customer)
    data['order_line'] = []
    data['images'] = Images.get_all_face_images()
    data['no_orders'] = len(data['orders'])==0    

    if not data['no_orders']:
        for order in data['orders']:
            data['order_line'].append(Order_Line.get_orderline(order.id))
    
    print(data)

    return render(request, "view-orders.html", data)
# -------------------------------------------------



# =====================================================
# ------------------ user management ------------------
# =====================================================

# account management
def account(request):

    if request.session.get('customer_email'):
        customer_email = request.session['customer_email']
        customer = Customer.get_customer_by_contact(customer_email)
    elif request.session.get('customer_phone'):
        customer_phone = request.session['customer_phone']
        customer = Customer.get_customer_by_contact(customer_phone)
        
    customer_name = customer.first_name+" "+customer.last_name



    data = {
        'title': "Healthify Nutrition",
        'user_name' : customer_name
    }

    return render(request, "account.html", data)


# signup/login --> user registeration
returnURL = None
def signup_login(request):
    
    email_list = list(Customer.objects.values_list("email", flat=True))
    phone_list = list(Customer.objects.values_list("phone", flat=True))
   
    data = {
        'title': "Healthify Nutrition",
        'can_login': False ,
        'need_to_sign_in' : False
    }

    if request.method == 'GET':
        global returnURL
        returnURL = request.GET.get('return_url')
        print("1---",returnURL)
        return render(request, "signup-login.html", data)

    else:
        print("2---",returnURL)
        post_data = request.POST
        email_phone = post_data.get('email-phone')

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        error_msg = None

        # email validation
        if (not email_phone):
            error_msg = "*Please enter your email or mobile number".title()

        elif (re.fullmatch(regex, email_phone)) or (email_phone.isnumeric() and len(email_phone)==10):
            error_msg = None

        else:
            error_msg = "*Please enter a valid email or mobile number".title()


        if(not error_msg):

            if email_phone in email_list+phone_list:
                data['email_phone'] = email_phone
                data['can_login'] = True
                received_password = post_data.get('password')

                if received_password:
                    customer = Customer.get_customer_by_contact(email_phone)
                    customer_password = customer.password
                    if received_password == customer_password:
                        if '@' in email_phone:
                            request.session['customer_email'] = email_phone
                        else:
                            request.session['customer_phone'] = email_phone
                        
                        print("3---",returnURL)
                        if returnURL =='/checkout':
                            cart = request.session.get('cart')
                            print(cart)
                            for id in cart:
                                qty = cart[id]
                                print(id,qty)
                                if Cart.is_product_in_cart(customer, id):
                                    cart_products = Cart.get_particular_product(customer, id)
                                    cart_products.qty += 1
                                    cart_products.register()
                                else:
                                    cart_instance = Cart(
                                        user=customer, 
                                        product=Product.get_product_by_id(id)[0],
                                        qty=qty
                                        )
                                    cart_instance.register()
                            request.session.cart = {}
                            return redirect('checkout')
                        else:
                            return redirect('home')
                    else:
                        data['password'] = received_password
                        data['error_msg'] = "*Please enter correct password"
                        return render(request, "signup-login.html", data)

                
                else:
                    return render(request, "signup-login.html", data)


            else:
                data['need_to_sign_in'] = True
                if '@' in email_phone:
                    data['email'] = email_phone
                else:
                    data['phone'] = email_phone
                return render(request, "signup.html", data)

            

        else:
            data['error_msg'] = error_msg
            data['email_phone'] = email_phone
            return render(request, "signup-login.html", data)


# signup
def signup(request):

    email_list = list(Customer.objects.values_list("email", flat=True))
    phone_list = list(Customer.objects.values_list("phone", flat=True))
   
    if request.method == 'GET':
        return redirect('signup-login')


    else:
        data = {
            'title' : "Healthify Nutrition"
        }

        post_data = request.POST

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


        # user details

        data['email'] = post_data.get('email')
        data['phone'] = post_data.get('phone')
        data['fname'] = post_data.get('fname')
        data['lname'] = post_data.get('lname')
        data['password'] = post_data.get('password')
        data['cpassword'] = post_data.get('cpassword')

        # error msgs
        data['email_error'] = None
        data['phone_error'] = None
        data['fname_error'] = None
        data['lname_error'] = None
        data['password_error'] = None
        data['cpassword_error'] = None

        


        if data['email'] in email_list:
            data['email_error'] = "*Email Already Registered"

        if data['phone'] in phone_list:
            data['phone_error'] = "*Phone Number Already Registered"

        
        if len(data['phone']) != 10 or (not data['phone'].isnumeric()):
            data['phone_error'] = "*Please Enter Correct Phone Number"
        
        if (not data['fname'].isalpha()):
            data['fname_error'] = "*First Name Should Contain only Characters"
        if len(data['fname'])<3:
            data['fname_error'] = "*First Name Should Contain Atleast 3 Characters"

        if (not data['lname'].isalpha()):
            data['lname_error'] = "*Last Name Should Contain only Characters"
        if len(data['lname'])<3:
            data['lname_error'] = "*Last Name Should Contain Atleast 3 Characters"

        if (not data['password'].count(" ")==0):
            data['password_error'] = "*Password Should Not Contain Space"
        if len(data['password'])<6:
            data['password_error'] = "*Password Should Contain Atleast 6 Characters/Numbers"

        if data['password']!=data['cpassword']:
            data['cpassword_error'] = "*Password Not Matching"

        
        form_has_error = data['email_error'] or data['phone_error'] or data['fname_error'] or data['lname_error'] or data['password_error'] or data['cpassword_error']

        if form_has_error:
            return render(request, "signup.html", data)
        
        else:
            customer = Customer(first_name = data['fname'],
                                last_name = data['lname'],
                                email = data['email'],
                                phone = data['phone'],
                                password = data['password'])
            customer.register()

            request.session['customer_email'] = data['email']
            
            
            print(returnURL)
            if returnURL =='/checkout':
                cart = request.session.get('cart')
                print(cart)
                for id in cart:
                    qty = cart[id]
                    print(id,qty)
                    if Cart.is_product_in_cart(customer, id):
                        cart_products = Cart.get_particular_product(customer, id)
                        cart_products.qty += 1
                        cart_products.register()
                    else:
                        cart_instance = Cart(
                            user=customer, 
                            product=Product.get_product_by_id(id)[0],
                            qty=qty
                            )
                        cart_instance.register()
                request.session.cart = {}
                return redirect('checkout')
            else:
                return redirect('home')
            


# logout
def logout(request):
    request.session.clear()
    return redirect('home')



    
    




    


   
    














        
        

