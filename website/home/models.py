from django.db import models

# Create your models here.

#Contact form
class Contact(models.Model):
    sno= models.AutoField(primary_key=True)
    name= models.CharField(max_length=255)
    phone= models.CharField(max_length=13)
    email= models.EmailField(max_length=100, null=True)
    subject= models.CharField(max_length=255)
    message= models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

  
#newsletter 

class Subscribers(models.Model):
    email = models.EmailField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    