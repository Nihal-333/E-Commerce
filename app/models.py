from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


STATE_CHOICES = (
    ('KA', 'Karnataka'), ('AP', 'Andhra Pradesh'), ('KL', 'Kerala'), ('TN', 'Tamil Nadu'), ('MH', 'Maharashtra'), ('UP', 'Uttar Pradesh'), ('GA', 'Goa'), ('GJ', 'Gujarat'), ('RJ', 'Rajasthan'), ('HP', 'Himachal Pradesh'), ('TG', 'Telangana'), ('AR', 'Arunachal Pradesh'), ('AS', 'Assam'), ('BR', 'Bihar'), ('CT', 'Chhattisgarh'), ('HR', 'Haryana'), ('JH', 'Jharkhand'), ('MP', 'Madhya Pradesh'), ('MN', 'Manipur'), ('ML', 'Meghalaya'), ('MZ', 'Mizoram'), ('NL', 'Nagaland'), ('OR', 'Odisha'), ('PB', 'Punjab'), ('SK', 'Sikkim'), ('TR', 'Tripura'), ('UT', 'Uttarakhand'), ('WB', 'West Bengal'), ('AN', 'Andaman and Nicobar Islands'), ('CH', 'Chandigarh'), ('DH', 'Dadra and Nagar Haveli and Daman and Diu'), ('DL', 'Delhi'), ('JK', 'Jammu and Kashmir'), ('LD', 'Lakshadweep'), ('LA', 'Ladakh'), ('PY', 'Puducherry')
    )

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    addres = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=70)

    def __str__(self):
        return self.name

CATEGORY_CHOICES = (
    ('fr_vegie', 'fruits_vegitables'),
    ('groc', 'Grocery_staples'),
    ('dailyess', 'Daily_essentials'),
    ('frozen', 'Dairy_frozen'),
    ('homecare', 'Home_care_Personal_care'),
    ('bedbath', 'Home_care_Personal_care'),
    ('electronics', 'electronics'),
    ('footwears', 'footwears')


)

class Product(models.Model):
    title = models.CharField(max_length=75)
    mrp = models.FloatField()
    selling_price = models.FloatField()
    desc = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    product_image = models.ImageField(upload_to = 'productimg')
    quantity = models.CharField(max_length=10, default="")

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quant = models.PositiveBigIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)

STATUS_CHOICES = (

    ('accepted', 'accepted'),
    ('packed', 'packed'),
    ('on the way', 'on the way'),
    ('delivered','delivered'),
    ('cancel', 'cancel')

)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="pending")

class Adrs(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    name = models.CharField(max_length=100)
    addres = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=70)