from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from django.forms import CharField

class Books(models.Model):
    title        = models.CharField(max_length=50, blank=False)
    author       = models.CharField(max_length=200, blank=True, null=True) 
    age_range    = models.ForeignKey('Age_range',on_delete=models.PROTECT) 
    img          = models.URLField(blank=True, null=True)
    googl_id     = models.CharField(max_length=20,blank=True,null=True)
    actual       = models.BooleanField(default=True)
    def __str__ (self):
        return f"{self.title} {self.id}"

    # to use later
class Author(models.Model):
    name        = models.CharField(max_length=50,blank=False)
    actual      = models.BooleanField(default=True)
    def __str__ (self):
        return f"{self.name}"  

class Age_range(models.Model):
    range      = models.CharField(max_length=25, blank=False)
    def __str__ (self):
        return f"{self.range}"
    
class Library (models.Model):
    book      = models.ForeignKey(Books, on_delete=models.PROTECT)
    user      = models.ForeignKey('UserProfile', on_delete=models.PROTECT)
    comment   = models.TextField(blank=True,null=True)
    addDate   = models.DateField(auto_now_add=True)
    def __str__ (self):
        return f"{self.book.title} owner {self.user.first_name} id {self.id}"

    


class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    geo_latitudes = models.FloatField(blank=True, null=True)
    geo_longitude = models.FloatField(blank=True, null=True)
    def __str__ (self):
        return f"Profile user: {self.user.username} id {self.id}"


class RentsBook(models.Model):
    rent_user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    book = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return f"id {self.id} Rent_user: {self.rent_user} book: {self.book.id} {self.book.book.title} {self.book.user} start_date: {self.start_date} "

    


class Message(models.Model):
    book = models.ForeignKey(Library, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='book_owner')
    rent_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='book_renter')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    text = models.CharField(max_length=250, blank=False)
    date_sent = models.DateTimeField(auto_now_add=True)
    date_read = models.DateTimeField(null=True, blank=True)
    read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.owner = self.book.user

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.book.title} owner {self.owner.user} sender {self.sender.user} {self.id} {self.read}"
 