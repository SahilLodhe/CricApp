from rest_framework import serializers
from .models import Player,IPLTeam,INTLTeam

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('__all__')
class IPLTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPLTeam
        fields = ('__all__')
class INTLTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = INTLTeam
        fields = ('__all__')
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['__all__']
# class ProfileExtendSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile_extend
#         fields = ['__all__']