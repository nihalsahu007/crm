from django.shortcuts import  render, redirect
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.http import *
from django.urls import reverse
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.contrib import messages
import random, string
import datetime
# import dateutil.parser
from django.utils.dateparse import parse_datetime
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


@login_required(login_url='/newapp/login/')
@require_http_methods(["GET"])
def index(request):
	if request.user.is_authenticated:
		searched_data = request.GET.get('search')
		sort_data = request.GET.get('sort')
		user_data_collection={}
		form=SearchForm(request.GET)
		users = User.objects.filter(userprofile__user_type="customer",note__note_created_by=request.user.id).exclude(username=request.user).order_by('id')
		if searched_data:
			searched_users = users.filter(username__contains=searched_data)
			if not searched_users.exists():
				searched_users = users.filter(userprofile__address__contains=searched_data)
			users = searched_users
		if sort_data:
			users = users.order_by("username")
		paginator = Paginator(users, 5)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		return render(request,'newapp/index.html',{"form":form,"page_obj":page_obj})
	# return HttpResponseRedirect(reverse('newapp:loggedin_view'))



@require_http_methods(["GET","POST"])
def register(request):
	if request.method=='POST':
		form=RegistrationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			confirm_password = form.cleaned_data['confirm_password']
			object_of_user = User.objects.create_user(username,email,password)
			UserProfile.objects.create(user_type = "telecaller" , address="string", phone_numnber="123", user=object_of_user)
			return HttpResponseRedirect(reverse('newapp:loggedin_view'))
	else:
		form = RegistrationForm()
	return render(request,'newapp/register.html', {'form': form})


@require_http_methods(["GET","POST"])
def loggedin(request):
	if request.method=='POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('/newapp',user)
	else:
		form = LoginForm()
	return render(request,'newapp/login.html', {'form': form})


def loggout(request):
    logout(request)
    return HttpResponseRedirect(reverse('newapp:loggedin_view'))


@login_required(login_url='/newapp/login/')
@require_http_methods(["GET","POST"])
def change_password(request):
	if request.user.is_authenticated:
		if request.method=='POST':
			form = ChangePasswordForm(request.POST,user=request.user)
			if form.is_valid():
				new_password = form.cleaned_data['new_password']
				password_change = User.objects.get(username=request.user.username)
				password_change.set_password(new_password)
				password_change.save()
				return HttpResponseRedirect(reverse('newapp:loggedin_view'))
		else:
			form = ChangePasswordForm(user=request.user)
		return render(request,'newapp/change_password.html',{'form' : form})


@login_required(login_url='/newapp/logixn/')
@require_http_methods(["GET","POST"])
def note(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = NoteForm(request.POST,request.FILES)
			if form.is_valid():
				name = form.cleaned_data['name']
				description = form.cleaned_data['description']
				address = form.cleaned_data['address']
				phone = form.cleaned_data['phone_numnber']

				image = request.FILES['image']
				print(name,description,address,phone,image)
				length = 5
				letters = string.ascii_lowercase
				password = ''.join(random.choice(letters) for i in range (length))
				print(password)
				last_string_of_email="@gmail.com"
				email = name + last_string_of_email
				print(email)
				object_of_user = User.objects.create_user(name, email, password)
				print(object_of_user)
				UserProfile.objects.create(user_type = "customer" , address=address, phone_numnber=phone, user=object_of_user,image=image)
				Note.objects.create(note_created_by= request.user, customer=object_of_user, description=description)
				return HttpResponseRedirect(reverse('newapp:index'))
		else:
			form = NoteForm()
	return render(request,'newapp/note.html',{'form' : form})


@login_required(login_url='/newapp/login/')
@require_http_methods(["GET","POST"])
def reminder(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = ReminderForm(request.POST, user=request.user.id)
			if form.is_valid():
				user_id = form.cleaned_data["customer"]
				call_time = form.cleaned_data["call_time"]
				later_time = form.cleaned_data['later_time']
				user = User.objects.get(id=user_id)
				reminder_obj = Reminder(customer=user,call_time=call_time,call_later=later_time)
				reminder_obj.save()
				return HttpResponseRedirect(reverse('newapp:index'))
		else:
			form = ReminderForm(user=request.user.id)
	return render(request,'newapp/reminder.html',{'form' : form})


@login_required(login_url='/newapp/login/')
@require_http_methods(["GET"])
def reminders(request):
	if  request.user.is_authenticated:
		reminders = Reminder.objects.order_by('-call_later')
		return render(request,'newapp/reminders.html',{'reminders' : reminders})



@login_required(login_url='/newapp/login/')
@require_http_methods(["GET"])
def follow_up(request,reminder_id):
	reminder_id=Reminder.objects.filter(id = reminder_id)
	print(reminder_id)
	if  reminder_id.exists():
		reminder_id.update(status = True)
		print("this is follow up here")
		return HttpResponse("Success True")
	else:
		return HttpResponse("success fail")

@login_required(login_url='/newapp/login/')
@require_http_methods(["GET","POST"])
def update(request,user_id):
	if  request.user.is_authenticated:
		user=User.objects.get(id=user_id)
		if request.method == 'POST':
			form = UpdateForm(request.POST,user_id=user_id)
			profile=user.userprofile
			# import pdb; pdb.set_trace();
			if form.is_valid():
				name = form.cleaned_data['name']
				description = form.cleaned_data['description']
				address = form.cleaned_data['address']
				phone = form.cleaned_data['phone']
				user.username=name
				user.save()
				user.note.description=description
				profile.address=address
				profile.phone_numnber=phone
				profile.save()
				user.note.save()
				return HttpResponse(reverse('newapp:index'))
			else:
				print(form.non_field_errors)
				# import pdb;pdb.set_trace();
				rendered = render_to_string('newapp/update.html',context={"form": form,"user":user_id},request=request)
				return HttpResponse(rendered)
		else:
			initial_dict = {
				"name" : user.note.customer,
				"description" : user.note.description,
				"address":user.userprofile.address,
				"phone": user.userprofile.phone_numnber
				}
			form=UpdateForm(user_id=user_id,initial = initial_dict)
		rendered = render_to_string('newapp/update.html',context={"form": form,"user":user_id},request=request)
		return HttpResponse(rendered)


@login_required(login_url='/newapp/login/')
@require_http_methods(["GET"])
def delete(request,user_id):
	if request.user.is_authenticated:
		User.objects.filter(id=user_id).delete()
		return HttpResponseRedirect(reverse('newapp:index'))




@require_http_methods(["GET","POST"])
def forgot_password_email(request):
	if request.method=="POST":
		form = ForgotPasswordEmailForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			user = User.objects.get(email=email)
			if user:
				subject = "Change passowrd request"
				from_mail = "abc@gmail.com"
				random_string = ''.join(random.choice(string.ascii_lowercase) for i in range (10))
				user.userprofile.random_string=random_string
				user.userprofile.save()
				message = f"http://127.0.0.1:8000/newapp/forgot_password/{random_string}"
				send_mail(subject,message,from_mail,['nihalgopaani@gmail.com'])
				return render(request,'newapp/reset_password_message_link.html')
	else:
		form = ForgotPasswordEmailForm()
	return render(request,'newapp/forgot_password_email.html',{'form':form})



@require_http_methods(["GET","POST"])
def forgot_password(request,random_string):
	# user = User.objects.filte(userprofile__random_string=random_string)
	# password_change = User.objects.get(username=user.username)
	if request.method == "POST":
		form = ForgotPasswordConfirmForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data['new_password']
			user = User.objects.get(userprofile__random_string=random_string)
			user.set_password(password)
			user.save()
			messages.success(request, 'password change successfully')
			return redirect(reverse('newapp:loggedin_view'))
	else:
		form = ForgotPasswordConfirmForm()
	return render(request,'newapp/password_reset_confirm.html',{"form":form})


@login_required(login_url='/newapp/login/')
@require_http_methods(["GET","POST"])
def update_reminder(request,user_id):
	if  request.user.is_authenticated:
		reminder=Reminder.objects.get(id=user_id)
		if request.method == 'POST':
			form = UpdateReminderForm(request.POST)
			if form.is_valid():
				call_time = form.cleaned_data['call_time']
				call_later = form.cleaned_data['call_later']
				reminder.call_time = call_time
				reminder.call_later = call_later
				reminder.save()

		else:
			initial_dict = {
				"name" : reminder.customer,
				"call_time" : reminder.call_time,
				"call_later" : reminder.call_later
				}
			form = UpdateReminderForm(initial = initial_dict)
		rendered = render_to_string('newapp/update_reminder.html',context={"form": form,'user':user_id},request=request)
		return HttpResponse(rendered)






# {% autoescape off %}
# <!DOCTYPE html>
# <html>
# <head>
# <title>Page Title</title>
# </head>
# <body>

# <h1>hello,</h1>
# <p>this link only one time for change password.</p>

# </body>
# </html>
# {% endautoescape %}

