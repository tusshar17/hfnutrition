from django.db import models
import datetime


class Category(models.Model):
    Category_Name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.Category_Name

    @staticmethod
    def get_categories():
        return Category.objects.all()

    def get_category_by_id(category_id):
        return Category.objects.filter(id=category_id)


class Brand(models.Model):
    Brand_Name = models.CharField(max_length=50)
    Brand_Contact = models.CharField(max_length=200, default="default")
    Brand_Email = models.EmailField(max_length=100, default="default")
    Brand_Logo = models.ImageField(upload_to='uploads/brands-logo')

    def __str__(self) -> str:
        return self.Brand_Name

    @staticmethod
    def get_brands():
        return Brand.objects.all()

    def get_brand_by_id(brand_id):
        return Brand.objects.filter(id=brand_id)


class Flavour(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def get_flavours():
        return Flavour.objects.all()


class Quantity(models.Model):
    value = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def get_quantities():
        return Quantity.objects.all()


class Product(models.Model):
    prod_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    flavour = models.ForeignKey(Flavour, on_delete=models.CASCADE)
    qty = models.ForeignKey(Quantity, on_delete=models.CASCADE)
    mrp = models.PositiveSmallIntegerField()
    selling_price = models.PositiveSmallIntegerField()
    stock = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.prod_name+"-"+self.brand.Brand_Name+"-" + \
            self.category.Category_Name+"-"+self.flavour.value+"-"+self.qty.value

    def get_products():
        return Product.objects.all()

    def get_trending_products():
        query = '''SELECT id, prod_name, category_id, brand_id, MIN(selling_price) 
                 FROM store_product 
                 GROUP BY prod_name'''
        return Product.objects.raw(query)

    def get_products_by_category(category_id):
        return Product.objects.filter(category=category_id)
    
    def get_products_by_category_sorted(category_id, sortBy):
        return Product.objects.filter(category=category_id).order_by(sortBy)

    def get_product_by_id(prod_id):
        return Product.objects.filter(id__in=prod_id)

    def get_variants(prod_name):
        return Product.objects.filter(prod_name=prod_name)



class Images(models.Model):

    IMG_CHOICES = [
        ('Face', 'Face'),
        ('Info', 'Info'),
        ('other', 'other')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='uploads/product-images/')
    img_type = models.CharField(max_length=10, choices=IMG_CHOICES)

    def get_images_by_prod(prod_id):
        return Images.objects.filter(product = prod_id)
    
    def get_info_img(prod_id):
        return Images.objects.filter(product = prod_id).filter(img_type = 'Info')
    
    def get_face_image(prod_id):
        return Images.objects.filter(product = prod_id).filter(img_type = 'Face')[0]
    
    def get_all_face_images():
        return Images.objects.filter(img_type = 'Face')
    
    



# =====================================================
# ------------------ user management ------------------
# =====================================================

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.email

    @staticmethod
    def get_customer_by_contact(email):
        if '@' in email:
            return Customer.objects.filter(email = email)[0]
        else:
            return Customer.objects.filter(phone = email)[0]


    def get_customers():
        return Customer.objects.all()
    
    def register(self):
        self.save()



class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)

    @staticmethod
    def get_cart_products(customer):
        return Cart.objects.filter(user = customer)
    
    @staticmethod
    def get_particular_product(customer, prod_id):
        return Cart.objects.filter(user = customer).filter(product = prod_id)[0]
    
    @staticmethod
    def is_product_in_cart(customer, prod_id):
        return Cart.objects.filter(user = customer).filter(product = prod_id).exists()
    
    def register(self):
        self.save()



# 
class Address_Book(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    pin = models.CharField(max_length=7)
    state = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def register(self):
        self.save()

    def __str__(self) -> str:
        return self.user.email+"-"+self.address

    @staticmethod
    def is_address_exists(customerid):
        return Address_Book.objects.filter(user=customerid).exists( )

    @staticmethod
    def get_customer_address(customerid):
        return Address_Book.objects.filter(user=customerid).order_by('-id')[0]




class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.today)
    time = models.TimeField(default=datetime.datetime.today)
    address = models.ForeignKey(Address_Book, on_delete=models.CASCADE)
    order_total = models.PositiveSmallIntegerField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Shipped', 'Shipped'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered')
    ]
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    def __str__(self) -> str:
        return str(self.id)+"-"+self.user.email
    
    @staticmethod
    def get_customer_orders(customer):
        return Order.objects.filter(user=customer).order_by('-id')

    def register(self):
        self.save()



class Order_Line(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField()
    qty = models.PositiveSmallIntegerField()

    def get_orderline(order_id):
        return Order_Line.objects.filter(order_id = order_id)

    def register(self):
        self.save()
