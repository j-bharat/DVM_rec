from django.contrib import admin
from .models import Profile 



admin.site.register(Profile)

class AccountAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                path('export/', views.export_profiles_to_xlsx, name='export'),
            ),
        ]


