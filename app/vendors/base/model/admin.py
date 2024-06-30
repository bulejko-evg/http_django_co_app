from django.contrib import admin
from django.conf import settings


class AdminBaseModel(admin.ModelAdmin):
    """Base calss for ModelAdmin"""

    empty_value_display = settings.EMPTY_VALUE

    def save_model(self, request, obj, form, change):
        """Save model with set created (Account) and updated (Account) fields."""
        if change:
            if hasattr(obj, "updated"):
                obj.updated = request.user
        else:
            if hasattr(obj, "created"):
                obj.created = request.user
        super().save_model(request, obj, form, change)