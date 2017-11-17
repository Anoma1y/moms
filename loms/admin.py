from django.contrib import admin
from loms.models import RouteLoading, NodeLoading, UserLoading


class RouteLoadingAdmin(admin.ModelAdmin):
	pass

class UserLoadingAdmin(admin.ModelAdmin):
	pass

admin.site.register(RouteLoading, RouteLoadingAdmin)
admin.site.register(UserLoading, UserLoadingAdmin)



# Register your models here.
