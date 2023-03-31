from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Book)
