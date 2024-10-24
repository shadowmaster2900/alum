# main_app/admin.py

from django.contrib import admin
from calendarapp.admin import EventAdmin, EventMemberAdmin
from accounts.admin import UserAdmin
from alumni.admin import (
    SchoolAdmin,
    AlumniCollectionAdmin,
    AlumniAdmin,
    NotificationAdmin,
    UserActionAdmin,
    send_birthday_emails_action,
)
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

class OTPAdmin(OTPAdminSite):
   pass
admin.site = OTPAdmin(name='OTPAdmin')
admin.site.register(TOTPDevice, TOTPDeviceAdmin)

# Register all admin models
admin.site.register(EventAdmin)
admin.site.register(EventMemberAdmin)
admin.site.register(UserAdmin)
admin.site.register(SchoolAdmin)
admin.site.register(AlumniCollectionAdmin)
admin.site.register(AlumniAdmin)
admin.site.register(NotificationAdmin)
admin.site.register(UserActionAdmin)
admin.site.register(TOTPDevice, TOTPDeviceAdmin)


# Optionally, you can define custom actions here
admin.site.add_action(send_birthday_emails_action, 'send_birthday_emails')
