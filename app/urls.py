from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('cart', views.show_cart, name='showcart'),
    path('pluscart', views.plus_cart),
    path('minuscart', views.minus_cart),
    path('removeitem', views.remove_item),
    path('buy', views.buy_now, name='buy-now'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('address', views.address, name='address'),
    path('orders', views.orders, name='orders'),
    path('changepassword', views.change_password, name='changepassword'),
    path('grocery', views.grocery, name='grocery'),
    path('dailyess', views.dailyess, name='dailyess'),
    path('fruits', views.fruits, name='fruits'),
    path('frozen', views.frozen, name='frozen'),
    path('homecare', views.homecare, name='homecare'),
    path('bedbath', views.bedbath, name='bedbath'),
    path('electronic', views.electronic, name='electronic'),
    path('footwears', views.footwears, name='footwears'),
    path('search', views.search, name="search"),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('customerregistration', views.customerregistration, name='customerregistration'),
    path('checkout', views.checkout, name='checkout'),  
    path('paymentdone', views.payment_done, name='paymentdone'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
