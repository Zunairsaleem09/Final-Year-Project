from django.db import models
from django.contrib.auth.models import User
from distutils.command.upload import upload
from email.policy import default
from django.utils import timezone
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class profile_edit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    title = models.CharField( max_length=200, null=True)
    desc_text = 'Hey, there this is default description about you that you can change'
    desc = models.CharField(default=desc_text, max_length=200, null=True)
    profile_img = models.ImageField(default='media/avatar.png', upload_to='media', null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    area = models.CharField(max_length=200, null=True)
    email = models.CharField( max_length=200, null=True)

    def __str__(self):
        return f"{self.user.username}"
    
# Create your models here.
class Product(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to="img")
    description = models.TextField()
    price = models.IntegerField()
    location = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    
    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="img")
    
    def __str__(self):
        return self.product.name

class chatMessages(models.Model):
    user_from = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    user_to = models.ForeignKey(User,
        on_delete=models.CASCADE,related_name="+")
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


    
# Parking Models
class reserve(models.Model):
    owner_name=models.CharField(max_length=200)
    address = models.CharField(max_length=150)
    phone = models.IntegerField()
    vehicle_brand=models.CharField(max_length=200)
    vehicle_name=models.CharField(max_length=200)
    vehicle_color=models.CharField(max_length=200)
    vehicle_no=models.CharField(max_length=200)
    vehicle_model=models.CharField(max_length=200)
    parking_time=models.IntegerField()
    license_no=models.CharField(max_length=12)
    cnic_no=models.CharField(max_length=13)
    def __str__(self):
        return self.owner_name
    
class parking_detail(models.Model):
    location=models.CharField(max_length=200)
    parking_area = models.CharField(max_length=200)
    available_parking_slots= models.CharField(max_length=200)
    total_parking_slots= models.CharField(max_length=200)
    charges=models.IntegerField()

    def __str__self(self):
        return self.parking_area