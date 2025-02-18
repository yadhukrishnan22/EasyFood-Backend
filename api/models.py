from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.contrib.auth.models import BaseUserManager
import random

class SellerManager(BaseUserManager):

    def get_by_natural_key(self, email):

        return self.get(email= email)
    

    
    def create_user(self, email, username, password=None, **extra_fields):

        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password) 
        user.save(using=self._db)
        return user



class BaseModel(models.Model):

    created_date = models.DateTimeField(auto_now_add= True)
    update_date = models.DateTimeField(auto_now_add= True)
    is_active = models.BooleanField(default = True)


class SellerCategory(BaseModel):

    seller_catname = models.CharField(max_length = 200)



class Seller(BaseModel, AbstractUser):

    objects = SellerManager()
    seller_category_choices = (
        ("Hotel","Hotel"),
        ("Hospital Canteen","Hospital Canteen"),
        ("College Canteen","College Canteen")
    )
    pin = models.CharField(max_length=6, unique=True, blank=True, null=True)
    seller_category = models.CharField(max_length=200,choices=seller_category_choices,
                            default="Hotel"
                            )
    
    def save(self, *args, **kwargs):
        if not self.pin:
            self.pin = self.generate_unique_pin()
        super().save(*args, **kwargs)

    def generate_unique_pin(self):
        return str(random.randint(100000, 999999))
    
    def __str__(self):
        return self.user.username


class SellerAccount(BaseModel):
    
    username = models.CharField(max_length=200)
    bio = models.CharField(max_length = 200, null = True)
    profile_picture = models.ImageField(upload_to = "profilepictures", null = True)
    address = models.TextField(null = True)
    owner = models.OneToOneField(Seller, on_delete= models.CASCADE, related_name = "profile")
    phone_number = models.CharField(max_length = 10)
    description = models.TextField(null = True)


def create_profile(sender, instance, created, **kwargs):
    if created:
        SellerAccount.objects.create(owner = instance)  
post_save.connect(create_profile,Seller)



class FoodCategory(BaseModel):

    food_category_name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    category_image = models.ImageField(upload_to='category_images', null = True)
    owner = models.ForeignKey(Seller, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'food_category_name'], name='unique_category')
        ]

class Food(BaseModel):

    food_name = models.CharField(max_length= 200)
    description = models.CharField(max_length= 200)
    food_image = models.ImageField(upload_to ='food_images', null= True)
    food_category_obj = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    owner = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places= 2)
    is_available = models.BooleanField(default = True)
    time_taken = models.PositiveIntegerField()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['owner', 'food_name'], name='unique_food')
        ]












