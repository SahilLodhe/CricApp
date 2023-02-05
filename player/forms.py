from dataclasses import fields
import imp
from pyexpat import model
from unittest.util import _MAX_LENGTH
from wsgiref.validate import validator
import django
from django.core import validators
from django import forms
from player.models import INTLTeam,IPLTeam,Player,User,Profile_extend
from django.contrib.auth.models import User
from . models import get_user_model
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    # first_name = forms.CharField(max_length=50)
    # last_name = forms.CharField(max_length=50)
    # Twitter = forms.URLField(max_length=300,required=False)
    # Facebook = forms.URLField(max_length=300,required=False)
    # Instagram = forms.URLField(max_length=300,required=False)
    # LinkedIn = forms.URLField(max_length=300,required=False)
    # Github = forms.URLField(max_length=300,required=False)
    # bio = forms.CharField(max_length=150)
    class Meta:
        fields = ("first_name","last_name","username", "email", "password1", "password2")
        # fields = ("__all__")
        model = get_user_model()
class UserUpdateForm(UserCreationForm):
    class Meta:
        fields = ("first_name","last_name", "email")
        # fields = ("__all__")
        model = get_user_model()

class EditUserForm(forms.ModelForm):
    class Meta:
        model = Profile_extend
        fields = ("Twitter","Facebook","Instagram","LinkedIn","Github","bio","birth_date","location")
        # fields = ("Twitter","Facebook","Instagram","LinkedIn","Github","bio","birth_date","location","user_img")
        # widgets = {
        #     'ownerplayer': forms.Select(attrs={'class': 'form-control'}),
        # }

class GiftPlayer(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('ownerplayer',)
        # widgets = {
        #     'ownerplayer': forms.Select(attrs={'class': 'form-control'}),
        # }

class PlayerCreationForm:
    class Meta:
        model = Player
        fields = ('ownerplayer',)
        widgets = {
            'ownerplayer' : forms.Select(attrs={'class':'form-control','label':'Owner'}),
        }