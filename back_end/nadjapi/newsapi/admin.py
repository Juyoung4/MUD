from django.contrib import admin
from .models import Articles, ArticlesFromApi
# Register your models here.

admin.site.register(Articles)
admin.site.register(ArticlesFromApi)