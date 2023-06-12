"""hfnutrition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from hfnutrition import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Product_Page, Cart_Page, CheckOut 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('category/<str:productCategory>-<str:categoryName>', views.product_category),
    path('category-sorted/<str:productCategory>-<str:categoryName>-<str:sortBy>', views.product_category_sorted),
    path('product/<str:productid>', Product_Page.as_view(), name="productPage"),
    path('signup-login', views.signup_login, name="signup-login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('account', views.account, name="account"),
    path('cart', Cart_Page.as_view(), name="cart"),
    path('checkout', CheckOut.as_view(), name="checkout"),
    path('order-placed', views.order_confirmed, name="oreder-confirmed"),
    path('my-orders', views.my_orders, name="view-orders")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

