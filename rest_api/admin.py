from django.contrib import admin
from .models import Company, Chat, CheckCode, Message, User, Job, Notification, CV
# Register your models here.

admin.site.register(Company)
admin.site.register(Chat)
admin.site.register(CheckCode)
admin.site.register(Message)
admin.site.register(Job)
admin.site.register(User)
admin.site.register(Notification)
admin.site.register(CV)