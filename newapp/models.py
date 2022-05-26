from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
	task=models.CharField(max_length=20)
	customer_name=models.CharField(max_length=128)
	phone=models.CharField(max_length=12)
	reason_of_left=models.CharField(max_length=200)

class Note(models.Model):
	note_created_by = models.ForeignKey(User,on_delete = models.CASCADE, related_name='note_created_by')
	customer = models.OneToOneField(User, on_delete = models.CASCADE)
	description = models.CharField(max_length=200)


class Reminder(models.Model):
	customer = models.OneToOneField(User, on_delete = models.CASCADE)
	call_time = models.DateTimeField()
	call_later = models.DateTimeField()
	status = models.BooleanField(default=False)

class UserProfile(models.Model):
	user_type = models.CharField(max_length=20)
	address = models.CharField(max_length=100)
	phone_numnber = models.CharField(max_length=12)
	random_string = models.CharField(max_length=200,default='')
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(upload_to="images")  

