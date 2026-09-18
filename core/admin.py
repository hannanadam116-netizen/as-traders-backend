from django.contrib import admin
from .models import BusinessProfile


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = (
        "business_name",
        "owner_name",
        "phone",
        "city",
        "state",
    )

    search_fields = (
        "business_name",
        "owner_name",
        "phone",
    )