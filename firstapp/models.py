from django.db import models
from django.contrib.auth.models import User
import datetime



class contact_us(models.Model):
    message = models.TextField()
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=250)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "contact_us"

class category(models.Model):
    cat_name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="media/%y/%m/%d")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name

class signup_model(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    profile_picture = models.ImageField(upload_to = "profiles/%y/%m/%d",null=True,blank=True)
    age = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    occupation = models.CharField(max_length=250,null=True,blank=True)
    gender = models.CharField(max_length=250,null=True)
    about = models.TextField(blank=True,null=True)
    added_on = models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Detail"

class add_property(models.Model):
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    property_name = models.CharField(max_length=250)
    property_category = models.ForeignKey(category,on_delete=models.CASCADE)
    property_price = models.FloatField()
    sale_price = models.FloatField()
    booking_amount = models.FloatField(null=True,blank=True)
    property_images = models.ImageField(upload_to="products/%y/%m/%d")
    image1 = models.FileField(upload_to="products/%y/%m/%d",null=True,blank=True)
    image2 = models.FileField(upload_to="products/%y/%m/%d",null=True,blank=True)
    image3 = models.FileField(upload_to="products/%y/%m/%d",null=True,blank=True)
    city = models.CharField(max_length=250)
    property_status = models.CharField(max_length=250,null=True,blank=True)
    area = models.FloatField(null=True,blank=True)
    no_of_bathroom = models.IntegerField()
    no_of_bedroom = models.IntegerField()
    is_air_conditioning = models.BooleanField(null=True,blank=True,default=False)
    is_gym = models.BooleanField(null=True,blank=True,default=False)
    is_laundry_room = models.BooleanField(null=True,blank=True,default=False)
    is_tv_cable = models.BooleanField(null=True,blank=True,default=False)
    is_wifi = models.BooleanField(null=True,blank=True,default=False)
    is_parking = models.BooleanField(null=True,blank=True,default=False)
    is_swimming_pool = models.BooleanField(null=True,blank=True,default=False)
    Balconies = models.IntegerField(null=True,blank=True)
    details = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.seller.username

class booked(models.Model):
    buyer=models.ForeignKey(signup_model,on_delete=models.CASCADE)
    prop=models.ForeignKey(add_property,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.prop.property_name

    class Meta:
        verbose_name_plural = "Book"
