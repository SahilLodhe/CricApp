from operator import index
from django.shortcuts import render
from player import views
from django.contrib import admin
from django.urls import path
# from numpy import place, r_
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from player import views
app_name = 'player'

urlpatterns = [
    path('',views.AboutView,name='about'),
    path('IPLTeamList/',views.IPLTeamListView.as_view(),name='IPLTeamList'),
    path('newiplteam/',views.CreateIPLTeam.as_view(),name='newiplteam'),
    path('IPLTeamDetail/<int:pk>/',views.IPLTeamDetailView.as_view(),name='IPLTeamDetail'),
    path('IPLTeamUpdate/<int:pk>/',views.IPLTeamUpdateView.as_view(),name='IPLTeamUpdate'),
    path('IPLTeamDelete/<int:pk>/',views.IPLTeamDeleteView.as_view(),name='IPLTeamDelete'),
    path('newintlteam/',views.CreateINTLTeam.as_view(),name='newintlteam'),
    path('INTLTeamList/',views.INTLTeamListView.as_view(),name='INTLTeamList'),
    path('INTLTeamDetail/<int:pk>',views.INTLTeamDetailView.as_view(),name='INTLTeamDetail'),
    path('INTLTeamUpdate/<int:pk>/',views.INTLTeamUpdateView.as_view(),name='INTLTeamUpdate'),
    path('INTLTeamDelete/<int:pk>/',views.INTLTeamDeleteView.as_view(),name='INTLTeamDelete'),
    path('newplayer/',views.CreatePLayer.as_view(),name='newplayer'),
    path('PlayerList/',views.PlayerList.as_view(),name='PlayerList'),
    path('PlayerDetail/<int:pk>/',views.PlayerDetailView.as_view(),name='PlayerDetail'),
    path('PlayerUpdate/<int:pk>/',views.PLayerUpdateView.as_view(),name='PlayerUpdate'),
    path('PlayerDelete/<int:pk>/',views.PLayerDeleteView.as_view(),name='PlayerDelete'),
    path('MyProfile/',views.my_profile,name='MyProfile'),
    path('Playersofintlteam/<int:pk>',views.get_players_of_intl_team,name='Playersofintlteam'),
    path('Playersofipllteam/<int:pk>',views.get_players_of_ipl_team,name='Playersofiplteam'),
    path('ODITeamX1/<int:pk>/',views.ODITeamX1,name='ODITeamX1'),
    path('TestTeamX1/<int:pk>/',views.TestTeamX1,name='TestTeamX1'),
    path('T20TeamX1/<int:pk>/',views.T20TeamX1,name='T20TeamX1'),
    path('IPLTeamX1/<int:pk>/',views.IPLTeamX1,name='IPLTeamX1'),
    path('GiftPlayer/<int:pk>/',views.gift_player,name="GiftPlayer"),
    path('MyT20TeamX1/',views.MyT20TeamX1,name='MyT20TeamX1'),
    path('MYIPLTeamX1/',views.MYIPLTeamX1,name='MYIPLTeamX1'),
    path('MyTestTeamX1/',views.MyTestTeamX1,name='MyTestTeamX1'),
    path('MyODITeamX1/',views.MyODITeamX1,name='MyODITeamX1'),
    path('worldODIXI/',views.worldODIXI,name='worldODIXI'),
    path('worldTestXI/',views.worldTestXI,name='worldTestXI'),
    path('worldT20XI/',views.worldT20XI,name='worldT20XI'),
    path('IPLXI/',views.IPLXI,name='IPLXI'),
    path('ExtraProfile/',views.ExtraProfile.as_view(),name='ExtraProfile'),
    path('ProfileUpdateView/',views.ProfileUpdateView.as_view(),name='ProfileUpdateView'),
    path('ViewStats/',views.ViewStats,name='ViewStats'),
    path('ViewMyStats/',views.viewuserStats,name='ViewMyStats'),
    path('search_venues/',views.search_venues,name='search_venues'),
]
