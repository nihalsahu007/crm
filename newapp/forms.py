from django import forms
from django.core.exceptions import ValidationError
# from django.core.exceptions import ValidationError
# from django.models import  
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from datetime import datetime    
from datetime import timedelta
from django.utils import timezone


class RegistrationForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	email = forms.EmailField(label='Email', max_length=20)
	password = forms.CharField(label = 'Password' , max_length=20,widget=forms.PasswordInput )
	confirm_password = forms.CharField(label = 'Confirm Password' , max_length=20, widget=forms.PasswordInput)
	
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if not User.objects.filter(username=username).exists():
			return username
		else:
			raise forms.ValidationError('Username ' + username + ' already exists')

	def clean(self):
		password = self.cleaned_data.get("password")
		confirm_password = self.cleaned_data.get("confirm_password")
		if password != confirm_password:
			raise forms.ValidationError("password and confirm_password mismatch")


class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=20)
	password = forms.CharField(label = 'Password' , max_length=20, widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super(LoginForm,self).clean()
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")
		if User.objects.filter(username=username).exists():
			user = User.objects.get(username=username)
			if not user.check_password(password):
				raise forms.ValidationError("password is incorrect")
		else:
			raise forms.ValidationError("username not exist")

	
class ChangePasswordForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

	old_password = forms.CharField(label = 'Old password', max_length = 20, widget=forms.PasswordInput)	
	new_password = forms.CharField(label = 'New password', max_length = 20, widget=forms.PasswordInput)
	confirm_password = forms.CharField(label = 'confirm_password' , max_length = 20, widget=forms.PasswordInput)

	def clean_old_password(self):
		old_password = self.cleaned_data.get("old_password")
		if User.objects.get(username=self.user).check_password(old_password):
			return old_password
		else:
			raise forms.ValidationError("Old password wrong")

	def clean(self):
		new_password = self.cleaned_data.get("new_password")
		confirm_password = self.cleaned_data.get("confirm_password")
		if new_password != confirm_password:
			raise forms.ValidationError("password and confirm_password mismatch")


class NoteForm(forms.Form):
	name = forms.CharField(label='Customer Name', max_length=20)
	description = forms.CharField(label='Description', max_length=200)
	address = forms.CharField(label= 'Address', max_length = 20)
	phone_numnber = forms.CharField(label = 'Phone Number', max_length = 12)
	image = forms.ImageField(label = 'Image  ' )
	def clean_name(self):
		name = self.cleaned_data.get('name')
		if not User.objects.filter(username=name).exists():
			return name
		else:
			raise forms.ValidationError('Username ' + name + ' already exists')
	

class ReminderForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(ReminderForm, self).__init__(*args, **kwargs)
		self.fields['customer'].choices = User.objects.filter(note__note_created_by = self.user).values_list('id',"username")
	customer = forms.ChoiceField(label = 'Name',widget=forms.Select(), required=True)
	call_time = forms.DateTimeField(label="Call Time",initial=datetime.now().strftime("%Y-%m-%d %I:%M:%S"), required=True)
	later_time = forms.DateTimeField(label="Later Time",initial=datetime.now().strftime("%Y-%m-%d %I:%M:%S"), required=True)
	



class UpdateForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.user_id = kwargs.pop('user_id')
		super(UpdateForm, self).__init__(*args, **kwargs)
	name = forms.CharField(label='Customer Name', max_length=20, required=True)
	phone = forms.CharField(label= 'Phone', max_length = 20, required=True)
	description = forms.CharField(label='Description', max_length=200, required=True)
	address = forms.CharField(label= 'Address', max_length = 20, required=True)
	
	def clean_name(self):
		name = self.cleaned_data.get('name')
		if User.objects.get(id=self.user_id).username == name:
			return name
		else:
			if not User.objects.filter(username=name).exists():
				return name
			else:
				raise forms.ValidationError("Username already taken")

FRUIT_CHOICES= [
	('', ''),
    ('name', 'Name')
    ]
class SearchForm(forms.Form):
	search = forms.CharField(label= 'Search',widget=forms.TextInput(attrs={'placeholder':'search'}),required=False)
	sort = forms.CharField(label='Name', widget=forms.Select(choices=FRUIT_CHOICES),required=False)	


class ForgotPasswordEmailForm(forms.Form):
	email = forms.EmailField(label='Email', max_length=20,required=False)
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exists():
			return email
		else:
			raise forms.ValidationError("Email not exists")			


class ForgotPasswordConfirmForm(forms.Form):
	new_password = forms.CharField(label = 'New password', max_length = 20, widget=forms.PasswordInput)
	confirm_password = forms.CharField(label = 'confirm_password' , max_length = 20, widget=forms.PasswordInput)
	def clean(self):
		new_password = self.cleaned_data.get("new_password")
		confirm_password = self.cleaned_data.get("confirm_password")
		if new_password != confirm_password:
			raise forms.ValidationError("password and confirm_password mismatch")
			
class UpdateReminderForm(forms.Form):
	name = forms.CharField(label="Name",disabled=True,required=False)
	# call_time = forms.DateTimeField(label="Call_Time",initial=datetime.now().strftime("%Y-%m-%d %I:%M:%S"), required=True)
	call_time = forms.DateTimeField(label="Call Time" ,widget=forms.DateTimeInput(format='%Y-%m-%d %I:%M:%S'),required=True)
	call_later = forms.DateTimeField(label="Later_Time",widget=forms.DateTimeInput(format='%Y-%m-%d %I:%M:%S'), required=True)
