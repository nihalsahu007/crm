from django.contrib import admin
from .models import *


class ReminderAdmin(admin.StackedInline):
	model = Reminder
	extra = 3

class NoteAdmin(admin.ModelAdmin):
	fieldsets= [
		(None, 				{'fields' : ['note_created_by']}),
		('Customer Name' , 	{'fields' : ['customer']}),
		('Description Here', {'fields' :['description']}),
	]
	list_display = ('note_created_by','customer','description')


admin.site.register(Contact)
admin.site.register(Note)
admin.site.register(Reminder)
admin.site.register(UserProfile)


# ['note_created_by','customer','description']