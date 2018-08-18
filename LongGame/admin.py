# Register your models here.

from django.contrib import admin
from .models import LongGame
from .models import PlayerList

admin.site.register(LongGame)
admin.site.register(PlayerList)
