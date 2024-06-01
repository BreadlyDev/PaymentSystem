from django.contrib import admin

from . import models as m

admin.site.register(m.App)
admin.site.register(m.AppCredentials)
