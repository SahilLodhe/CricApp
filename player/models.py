from distutils.command.upload import upload
from email.policy import default
# from pickletools import read_unicodestring1
# from pyexpat import model
# from random import choices
# import re
# from statistics import mode
# from tokenize import blank_re
# from typing_extensions import Self


from django.db import models
from wsgiref.validate import validator
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()
# Create your models here.
# class Profile(models.Model):  
#     user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)  
#     #other fields here
#     # img = models.ImageField(upload_to='user',default='user/default.jpg')
#     Twitter = models.URLField(max_length=300,blank=True,default="")
#     Facebook = models.URLField(max_length=300,blank=True,default="")
#     Instagram = models.URLField(max_length=300,blank=True,default="")
#     LinkedIn = models.URLField(max_length=300,blank=True,default="")
#     Github = models.URLField(max_length=300,blank=True,default="")
#     bio = models.CharField(max_length=150,blank=True,default="")
#     birth_date = models.DateField(blank=True,null=True,default="")
#     location = models.CharField(max_length=50,blank=True,default="")
#     # user_img = models.ImageField(upload_to='user',default='user/default.jpg')
#     # upload_to='players',default='players/default.jpg'

#     def __str__(self):  
#         return "%s's profile" % self.user

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()  

class Profile_extend(models.Model):  
    user = models.OneToOneField(User,related_name='profile',on_delete=models.CASCADE)  
    #other fields here
    # img = models.ImageField(upload_to='user',default='user/default.jpg')
    img = models.ImageField(upload_to='user',blank = False,default='user/default.jpg')
    Twitter = models.URLField(max_length=300,blank=True,default="")
    Facebook = models.URLField(max_length=300,blank=True,default="")
    Instagram = models.URLField(max_length=300,blank=True,default="")
    LinkedIn = models.URLField(max_length=300,blank=True,default="")
    Github = models.URLField(max_length=300,blank=True,default="")
    bio = models.CharField(max_length=150,blank=True,default="")
    birth_date = models.DateField(blank=True,null=True)
    location = models.CharField(max_length=50,blank=True,default="")
    # user_img = models.ImageField(upload_to='user',default='user/default.jpg')
    # upload_to='players',default='players/default.jpg'

    def __str__(self):  
        return "%s's profile" % self.user

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile_extend.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.Profile_extend.save()

class IPLTeam(models.Model):

    owner = models.ForeignKey('auth.User',on_delete=models.CASCADE,null=True, blank=True,related_name='rel_ownerIPL')
    name = models.CharField(max_length=40)
    flagipl = models.ImageField(upload_to='ipl',blank = False,default=0)
    matches_played = models.IntegerField(default=0)
    matches_won = models.IntegerField(default=0)
    matches_lost = models.IntegerField(default=0)
    trophies_won = models.IntegerField(default=0)
    def get_absolute_url(self):
        return reverse("player:about")
    def __str__(self):
        return self.name
    # def count_teams(self):
    #     return self.objects.count
    def win_p(self):
        return (self.matches_won/self.matches_played)*100

    
    
class INTLTeam(models.Model):

    ownerINTL = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name='rel_ownerINTL',null=True, blank=True)
    name = models.CharField(max_length=20)
    flagintl = models.ImageField(upload_to='intl',blank = False,default=0)
    World_cups_won = models.IntegerField()
    Champion_trophies_won = models.IntegerField()
    T20WC_trophies_won = models.IntegerField()
    Asia_Cups_Won = models.IntegerField()
    ODI_matches_played = models.IntegerField()
    Test_matches_played = models.IntegerField()
    T20_matches_played = models.IntegerField()
    # flag = models.ImageField()
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("player:about")
    

class Player(models.Model):

    # id = models.IntegerField(primary_key=True)
    ownerplayer = models.ForeignKey('auth.User',on_delete=models.CASCADE,default=User,related_name='rel_ownerplayer')
    name = models.CharField(max_length=20,unique=True)
    player_image = models.ImageField(upload_to='players',default='players/default.jpg')
    iplteam = models.ForeignKey(IPLTeam,on_delete=models.CASCADE,related_name='iplplayer',null=True,blank=True)
    intlteam = models.ForeignKey(INTLTeam,on_delete=models.CASCADE,related_name='intl_player',null=True,blank=True)
    # players_gifted = models.IntegerField(default=0)
    # players_recieved = models.IntegerField(default=0)
    age = models.IntegerField()
    jersey_number = models.IntegerField(default=0) 
    ROLE_CHOICES = (("Batsman","Batsman"), ("Batting Allrounder","Batting Allrounder"),
    ("Bowling Allrounder","Bowling Allrounder"), ("Fast Bowler","Fast Bowler"),
    ("Spin Bowler","Spin Bowler"),("cheerleader","cheerleader"))
    Role = models.CharField(max_length=25,choices = ROLE_CHOICES,default="cheerleader")
    BATTING_POSITIONS = (("Opener","Opener"),("Middle Order","Middle Order"),("Finisher","Finisher"),("Tailender","Tailender"))
    batting_position = models.CharField(max_length=25,choices=BATTING_POSITIONS,default="Tailender")
    
    ODIs_played = models.IntegerField(default=0)
    ODIs_innings_played = models.IntegerField(default=0)
    highest_scoreODI = models.IntegerField(default=0,blank=True)
    total_runsODI = models.IntegerField(default=0)
    total_balls_facedODI = models.IntegerField(default=0)
    not_outsODI = models.IntegerField(default=0)
    # ducksODI = models.IntegerField(default=0)
    # foursODI = models.IntegerField(default=0)
    # sixesODI = models.IntegerField(default=0)
    fiftiesODI = models.IntegerField(default=0)
    hundredsODI = models.IntegerField(default=0)
    innings_bowled_ODI = models.IntegerField(default=0)
    total_bowlsODI = models.IntegerField(default=0)
    total_runs_givenODI = models.IntegerField(default=0)
    wicketsODI = models.IntegerField(default=0)

    IPLs_played = models.IntegerField(default=0)
    IPLs_innings_played = models.IntegerField(default=0)
    highest_scoreIPL = models.IntegerField(default=0,blank=True)
    total_runsIPL = models.IntegerField(default=0)
    total_balls_facedIPL = models.IntegerField(default=0)
    not_outsIPL = models.IntegerField(default=0)
    # ducksIPL = models.IntegerField(default=0)
    # foursIPL = models.IntegerField(default=0)
    # sixesIPL = models.IntegerField(default=0)
    fiftiesIPL = models.IntegerField(default=0)
    hundredsIPL = models.IntegerField(default=0)
    innings_bowled_IPL = models.IntegerField(default=0)
    total_bowlsIPL = models.IntegerField(default=0)
    total_runs_givenIPL = models.IntegerField(default=0)
    wicketsIPL = models.IntegerField(default=0)

    Tests_played = models.IntegerField(default=0)
    Tests_innings_played = models.IntegerField(default=0)
    highest_scoreTest = models.IntegerField(default=0,blank=True)
    total_runsTest = models.IntegerField(default=0)
    total_balls_facedTest = models.IntegerField(default=0)
    not_outsTest = models.IntegerField(default=0)
    # ducksTest = models.IntegerField(default=0)
    # foursTest = models.IntegerField(default=0)
    # sixesTest = models.IntegerField(default=0)
    fiftiesTest = models.IntegerField(default=0)
    hundredsTest = models.IntegerField(default=0)
    innings_bowled_Test = models.IntegerField(default=0)
    total_bowlsTest = models.IntegerField(default=0)
    total_runs_givenTest = models.IntegerField(default=0)
    wicketsTest = models.IntegerField(default=0)

    T20s_played = models.IntegerField(default=0)
    T20s_innings_played = models.IntegerField(default=0)
    highest_scoreT20 = models.IntegerField(default=0,blank=True)
    total_runsT20 = models.IntegerField(default=0)
    total_balls_facedT20 = models.IntegerField(default=0)
    not_outsT20 = models.IntegerField(default=0)
    # ducksT20 = models.IntegerField(default=0)
    # foursT20 = models.IntegerField(default=0)
    # sixesT20 = models.IntegerField(default=0)
    fiftiesT20 = models.IntegerField(default=0)
    hundredsT20 = models.IntegerField(default=0)
    innings_bowled_T20 = models.IntegerField(default=0)
    total_bowlsT20 = models.IntegerField(default=0)
    total_runs_givenT20 = models.IntegerField(default=0)
    wicketsT20 = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("player:about")


    def get_SR_ODI(self):
        if self.total_balls_facedODI == 0:
            return 0
        else:
            return (self.total_runsODI/self.total_balls_facedODI)*100
    def get_SR_IPL(self):
        if self.total_balls_facedIPL == 0:
            return 0
        else:
            return (self.total_runsIPL/self.total_balls_facedIPL)*100
    def get_SR_Test(self):
        if self.total_balls_facedTest == 0:
            return 0
        else:
            return (self.total_runsTest/self.total_balls_facedTest)*100
    def get_SR_T20(self):
        if self.total_balls_facedT20 == 0:
            return 0
        else:
            return (self.total_runsT20/self.total_balls_facedT20)*100

    def get_bat_avg_ODI(self):
        if self.ODIs_innings_played - self.not_outsODI == 0:
            return 0
        else:
            return(self.total_runsODI/(self.ODIs_innings_played - self.not_outsODI))
    def get_bat_avg_IPL(self):
        if self.IPLs_innings_played - self.not_outsIPL == 0:
            return 0
        else:
            return(self.total_runsIPL/(self.IPLs_innings_played - self.not_outsIPL))
    def get_bat_avg_Test(self):
        if self.Tests_innings_played - self.not_outsTest == 0:
            return 0
        else:
            return(self.total_runsTest/(self.Tests_innings_played - self.not_outsTest))
    def get_bat_avg_T20(self):
        if self.T20s_innings_played - self.T20s_played == 0:
            return 0
        else:
            return(self.total_runsT20/(self.T20s_innings_played - self.T20s_played))

    def get_economy_ODI(self):
        if self.total_bowlsODI == 0:
            return 0
        else:
            return (self.total_runs_givenODI/self.total_bowlsODI)*6
    def get_economy_IPL(self):
        if self.total_bowlsIPL == 0:
            return 0
        else:
            return (self.total_runs_givenIPL/self.total_bowlsIPL)*6
    def get_economy_Test(self):
        if self.total_bowlsTest == 0:
            return 0
        else:
            return (self.total_runs_givenTest/self.total_bowlsTest)*6
    def get_economy_T20(self):
        if self.total_bowlsT20 == 0:
            return 0
        else:
            return (self.total_runs_givenT20/self.total_bowlsT20)*6

    def get_bowl_avgODI(self):
        if self.wicketsODI == 0:
            return 0
        else:
            return self.total_runs_givenODI/self.wicketsODI
    def get_bowl_avgIPL(self):
        if self.wicketsIPL == 0:
            return 0
        else:
            return self.total_runs_givenIPL/self.wicketsIPL
    def get_bowl_avgTest(self):
        if self.wicketsTest == 0:
            return 0
        else:
            return self.total_runs_givenTest/self.wicketsTest
    def get_bowl_avgT20(self):
        if self.wicketsT20 == 0:
            return 0
        else:
            return self.total_runs_givenT20/self.wicketsT20

    def get_bowl_SRODI(self):
        if self.wicketsODI == 0:
            return 0
        else:
            return self.total_bowlsODI/self.wicketsODI
    def get_bowl_SRIPL(self):
        if self.wicketsIPL == 0:
            return 0
        else:
            return self.total_bowlsIPL/self.wicketsIPL
    def get_bowl_SRTest(self):
        if self.wicketsTest == 0:
            return 0
        else:
            return self.total_bowlsTest/self.wicketsTest
    def get_bowl_SRT20(self):
        if self.wicketsT20 == 0:
            return 0
        else:
            return self.total_bowlsT20/self.wicketsT20