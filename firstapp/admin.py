from django.contrib import admin
from firstapp.models import contact_us,signup_model,category,add_property,booked

admin.site.site_header = "FLATCHAT WEBSITE"

class contact_usAdmin(admin.ModelAdmin):
    list_display = ["id","name","email","subject","message","added_on"]
    search_fields = ["name"]
    list_filter = ["added_on","name"]

class categoryAdmin(admin.ModelAdmin):
    list_display = ["id","cat_name","description","added_on"]


admin.site.register(contact_us,contact_usAdmin)
admin.site.register(category,categoryAdmin)
admin.site.register(signup_model)
admin.site.register(add_property)
admin.site.register(booked)



