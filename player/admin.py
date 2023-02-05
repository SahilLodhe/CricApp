from django.contrib import admin
from player.models import IPLTeam,INTLTeam,Player,Profile_extend
# from player.models import IPLTeam,INTLTeam,Player,Profile
# Register your models here.
admin.site.register(Player)
admin.site.register(INTLTeam)
admin.site.register(IPLTeam)
admin.site.register(Profile_extend)
# admin.site.register(Profile)