from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'newapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('note/', views.note, name='note'),
    path('register/', views.register, name='register'),
    path('login/',views.loggedin, name='loggedin_view'),
    path('logout/',views.loggout, name='logout'),
    path('change_password/',views.change_password, name='change_password'),
    path('follow_up/<int:reminder_id>/',views.follow_up, name='follow_up'),
    path('reminder/',views.reminder, name='reminder'),
    path('reminders/',views.reminders, name='reminders'),
    path('update_reminder/<int:user_id>',views.update_reminder, name='update_reminder'), 
    path('update/<int:user_id>',views.update, name='update'),
    path('delete/<int:user_id>',views.delete, name='delete'),
    path('forgot_password_email',views.forgot_password_email, name='forgot_password_email'),
    path('forgot_password/<str:random_string>/', views.forgot_password, name="forgot_password"),
    
    # path('password_reset_complete/',views.password_reset_complete,name='password_reset_complete')
]
