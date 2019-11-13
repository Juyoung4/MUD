from django.contrib import admin
from .models import NewsSummary, Cluster, User, UserRating, Favorite, Recommend

# Register your models here.
admin.site.register(NewsSummary)
admin.site.register(Cluster)
admin.site.register(User)
admin.site.register(UserRating)
admin.site.register(Favorite)
admin.site.register(Recommend)