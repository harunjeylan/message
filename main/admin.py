from django.contrib import admin
from .models import Profile, UserFriend, Messages
# Register your models here.



class UserFriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'friends')
class MessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'bitween', 'text')


admin.site.register(Profile)
admin.site.register(UserFriend, UserFriendAdmin)
admin.site.register(Messages, MessagesAdmin)
