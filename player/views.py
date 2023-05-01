from django import http
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils import timezone
# from matplotlib.style import context  # changed for env311
# from numpy import sort  # changed for env311
from player import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
# FOR MTV
from player.models import INTLTeam,IPLTeam,Player,User,Profile_extend
# from player.forms import UserCreateForm,GiftPlayer,EditUserForm,UserUpdateForm,PlayerCreationForm
from player.forms import UserCreateForm,GiftPlayer,UserUpdateForm,PlayerCreationForm,EditUserForm
# FOR CBV
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
# for REST API
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.generics import ListAPIView
from .serializer import PlayerSerializer,INTLTeamSerializer,IPLTeamSerializer, UserSerializer, ProfileExtendSerializer

usernameglobal = get_user_model()
# Create your views here.

# REST API
class PlayerView(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
class INTLTeamView(viewsets.ModelViewSet):
    serializer_class = INTLTeamSerializer
    queryset = INTLTeam.objects.all()
class IPLTeamView(viewsets.ModelViewSet):
    serializer_class = IPLTeamSerializer
    queryset = IPLTeam.objects.all()
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
class ProfileExtendView(viewsets.ModelViewSet):
    serializer_class = ProfileExtendSerializer
    queryset = Profile_extend.objects.all()

# REST API ENDED

def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        players = Player.objects.filter(name__contains=searched)
        return render(request, 'registration/search_venues.html',{'searched':searched,'players':players})
    else:
        return render(request, 'registration/search_venues.html',{})


class ExtraProfile(CreateView):
    model = Profile_extend
    # Profile.objects.create(user=request.user)
    # fields = ['Twitter','Facebook','Instagram','LinkedIn','Github','bio','birth_date','location']
    fields = '__all__'

class AboutView(TemplateView):
    template_name = 'registration/about.html'

class TestPage(TemplateView):
    template_name = 'registration/test.html'

class ThanksPage(TemplateView):
    template_name = 'registration/thanks.html'

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class CreateIPLTeam(CreateView):# this needs a default template "modelname_form"
    model = IPLTeam
    fields = '__all__'
    # form_class = IPLTeamForm
    

class IPLTeamListView(ListView):# this needs a default template "modelname_list"
    model = IPLTeam
    context_object_name = 'IPLTeam_list'
    no_of_teams = IPLTeam.objects.count()
    extra_context = {'no_of_teams' : no_of_teams}
    
    def get_queryset(self):
        return IPLTeam.objects.order_by('trophies_won')

class IPLTeamDetailView(DetailView,LoginRequiredMixin):# this needs a default template "modelname_detail"
    model = IPLTeam
    context_object_name = 'iplteam'



class IPLTeamUpdateView(UpdateView,LoginRequiredMixin):
    model = IPLTeam
    fields = ['matches_played','matches_won','matches_lost','trophies_won']
    success_url = "/"
class IPLTeamDeleteView(DeleteView,LoginRequiredMixin):
    model = IPLTeam
    success_url = reverse_lazy('player:IPLTeamList')

class CreateINTLTeam(CreateView,LoginRequiredMixin):# this needs a default template "modelname_form"
    model = INTLTeam
    fields = '__all__'
    # template_name='player/intlteam_form.html'

class INTLTeamListView(ListView,LoginRequiredMixin):# this needs a default template "modelname_list"
    model = INTLTeam
    context_object_name = 'INTLTeam_list'
    no_of_teams = INTLTeam.objects.count()
    extra_context = {'no_of_teams' : no_of_teams}
    
    # def get_queryset(self):
    #     return INTLTeam.objects.order_by('trophies_won')
class INTLTeamDetailView(DetailView,LoginRequiredMixin):# this needs a default template "modelname_detail"
    model = INTLTeam
    context_object_name = 'intlteam'

# def INTLTeamDetailView(request,id):
#     model = IPLTeam
#     context = {}
#     context['data'] = IPLTeam.objects.get(id = id)
#     return render(request,'player/intlteam_detail.html')

class INTLTeamUpdateView(UpdateView,LoginRequiredMixin):
    model = INTLTeam
    # fields = ['World_cups_won','Champion_trophies_won','T20WC_trophies_won','Asia_Cups_Won','ODI_matches_played','Test_matches_played','T20_matches_played','flagintl']
    fields = ['World_cups_won','Champion_trophies_won','T20WC_trophies_won','Asia_Cups_Won','ODI_matches_played','Test_matches_played','T20_matches_played']
    success_url = "/"

class INTLTeamDeleteView(DeleteView,LoginRequiredMixin):
    model = INTLTeam
    success_url = reverse_lazy('player:IPLTeamList')

class CreatePLayer(CreateView,LoginRequiredMixin):# this needs a default template "modelname_form"
    model = Player
    form = PlayerCreationForm
    fields = '__all__'
    # fields = ['name','player_image',
    # 'iplteam','intlteam','age','jersey_number',
    # 'Role','batting_position','ODIs_played',
    # 'ODIs_innings_played','highest_scoreODI',
    # 'total_runsODI','total_balls_facedODI',
    # 'not_outsODI','fiftiesODI','hundredsODI',
    # 'innings_bowled_ODI','total_bowlsODI',
    # 'total_runs_givenODI','wicketsODI','IPLs_played',
    # 'IPLs_innings_played','highest_scoreIPL',
    # 'total_runsIPL','total_balls_facedIPL',
    # 'not_outsIPL','fiftiesIPL','hundredsIPL',
    # 'innings_bowled_IPL','total_bowlsIPL',
    # 'total_runs_givenIPL','wicketsIPL','Tests_played',
    # 'Tests_innings_played','highest_scoreTest',
    # 'total_runsTest','total_balls_facedTest',
    # 'not_outsTest','fiftiesTest','hundredsTest',
    # 'innings_bowled_Test','total_bowlsTest',
    # 'total_runs_givenTest','wicketsTest',
    # 'T20s_played','T20s_innings_played',
    # 'highest_scoreT20','total_runsT20',
    # 'total_balls_facedT20','not_outsT20','fiftiesT20',
    # 'hundredsT20','innings_bowled_T20','total_bowlsT20',
    # 'total_runs_givenT20','wicketsT20']
        
class PlayerDetailView(DetailView,LoginRequiredMixin):# this needs a default template "modelname_detail"
    model = Player
    context_object_name = 'player'

class PlayerList(ListView,LoginRequiredMixin):
    model = Player
    context_object_name = 'player_list'
    Batsman = "Batsman"
    Batting_Allrounder = "Batting Allrounder"
    Bowling_Allrounder = "Bowling Allrounder"
    Fast_Bowler = "Fast Bowler"
    Spin_Bowler = "Spin Bowler"
    no_of_players = Player.objects.all().count()
    # batsman = Player.objects.all().filter('player__Role__exact=Batsman')
    # batting_Allrounder = Player.objects.all().filter('player__Role__exact=Batting_Allrounder')
    # bowling_Allrounder = Player.objects.all().filter('player__Role__exact=Bowling_Allrounder')
    # fast_Bowler = Player.objects.all().filter('player__Role__exact=Fast_Bowler')
    # spin_Bowler = Player.objects.all().filter('player__Role__exact=Spin_Bowler')
  
    extra_context = {
        'no_of_players' : no_of_players,
        # 'batsman' : batsman,
        # 'battingAllrounder' : batting_Allrounder,
        # 'bowlingAllrounder' : bowling_Allrounder,
        # 'fastBowler' : fast_Bowler,
        # 'spinBowler' : spin_Bowler,
    }

class PLayerUpdateView(UpdateView,LoginRequiredMixin):
    model = Player
    fields = '__all__'
    success_url = "/"

class PLayerDeleteView(DeleteView,LoginRequiredMixin):
    model = Player
    success_url = reverse_lazy('player:about')





    # iplteam = models.ForeignKey(IPLTeam,on_delete=models.CASCADE)
    # intlteam = models.ForeignKey(INTLTeam,on_delete=models.CASCADE)
    # name = models.CharField(max_length=20)
    # age = models.IntegerField()
    # highest_score = models.IntegerField()
    # total_runs = models.IntegerField()
    # not_outs = models.IntegerField()
    # bat_avg = models.IntegerField()
    # total_bowls = models.IntegerField()
    # wickets = models.IntegerField()
    # bowl_avg = models.IntegerField()
    # jersey_number = models.IntegerField(default=0)   

# def signup(request):

#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         password2 = request.POST['password2']

#         if password == password2:
#             if User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email Taken')
#                 return redirect('signup')
#             elif User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username Taken')
#                 return redirect('signup')
#             else:
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 user.save()

#                 #log user in and redirect to settings page
#                 user_login = auth.authenticate(username=username, password=password)
#                 auth.login(request, user_login)


#                 return redirect('player:PlayerList')
#         else:
#             messages.info(request, 'Password Not Matching')
#             return redirect('signup')
        
#     else:
#         return render(request, 'registration/signup.html')

# @login_required
# def signin(request):
    
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)

#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             messages.info(request, 'Credentials Invalid')
#             return redirect('signin')

#     else:
#         return render(request, 'signin.html')

# @login_required(login_url='signin')
# def logout(request):
#     auth.logout(request)
#     return redirect('signin')

# @login_required
# def indian_players(request):
#     model = INTLTeam
#     context = {}
#     India = "India"
#     # context['dataset'] = Player.objects.all().order_by('get_bat_avg_ODI()').filter(intlteam__name__exact=India)
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=India), key=lambda x: x.get_bat_avg_ODI())
#     return render(request,'intlteamplayers/playersofteam.html',context)
# @login_required
# def australian_players(request):
#     model = INTLTeam
#     context = {}
#     Australia = "Australia"
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=Australia), key=lambda x: x.get_bat_avg_ODI())
    
#     return render(request,'intlteamplayers/playersofteam.html',context)
# @login_required
# def kiwi_players(request):
#     model = INTLTeam
#     context = {}
#     NewZealand = "New Zealand"
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=NewZealand), key=lambda x: x.get_bat_avg_ODI())
    
#     return render(request,'intlteamplayers/playersofteam.html',context)
# @login_required
# def southafrica_players(request):
#     model = INTLTeam
#     context = {}
#     SouthAfrica = "South Africa"
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=SouthAfrica), key=lambda x: x.get_bat_avg_ODI())
    
#     return render(request,'intlteamplayers/playersofteam.html',context)
# @login_required
# def england_players(request):
#     model = INTLTeam
#     context = {}
#     England = "England"
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=England), key=lambda x: x.get_bat_avg_ODI())
    
#     return render(request,'intlteamplayers/playersofteam.html',context)
# @login_required
# def srilanka_players(request):
#     model = INTLTeam
#     context = {}
#     Srilanka = "Sri Lanka"
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=Srilanka), key=lambda x: x.get_bat_avg_ODI())
    
#     return render(request,'intlteamplayers/playersofteam.html',context)
# @login_required
# def pakistan_players(request):
#     model = INTLTeam
#     context = {}
#     Pakistan = "Pakistan"
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=Pakistan), key=lambda x: x.get_bat_avg_ODI())
    
#     return render(request,'intlteamplayers/playersofteam.html',context)
# @login_required
# def westindies_players(request):
#     model = INTLTeam
#     context = {}
#     WestIndies = "West Indies"
#     context['dataset'] = sorted(Player.objects.all().filter(intlteam__name__exact=WestIndies), key=lambda x: x.get_bat_avg_ODI())
    
#     return render(request,'intlteamplayers/playersofteam.html',context)

@login_required
def get_players_of_intl_team(request,pk:int):
    model = INTLTeam,Player
    context = {}
    context['team'] = INTLTeam.objects.get(pk=pk)
    context['players'] = Player.objects.all()
    return render(request,'intlteamplayers/players_of_intl_team.html',context)
@login_required
def get_players_of_ipl_team(request,pk:int):
    model = IPLTeam,Player
    context = {}
    context['team'] = IPLTeam.objects.get(pk=pk)
    context['players'] = Player.objects.all()
    return render(request,'iplteamplayers/players_of_ipl_team.html',context)

def my_profile(request):
    model = Player,User
    my_players = User.objects.all().filter(rel_ownerplayer__ownerplayer=request.user)
    context = {}
    context['dataset'] = Player.objects.all()
    context['my_players'] = len(my_players)
    return render(request,'registration/my_profile.html',context)

def edit_profile(request,user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserUpdateForm
    profile_form = EditUserForm
    template_name = 'registration/profile.html'

    def post(self, request):

        post_data = request.POST or None

        user_form = UserUpdateForm(post_data, instance=request.user)
        profile_form = EditUserForm(post_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect("/")

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context) 

def gift_player(request,pk:int):
    context = {}
    model = Player
    obj = get_object_or_404(Player,pk=pk)
    form = GiftPlayer(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/")
    context["form"] = form
    context["player"] = obj
    return render(request,"gift/gift_form.html",context)

def worldODIXI(request):
    model = Player
    # getting the best openers
    openers = sorted(Player.objects.all().filter(batting_position__exact="Opener").filter(ODIs_played__gt=80),key = lambda x: -x.get_bat_avg_ODI()) # the negative sign before x.get_bat_avg_ODI is for sorting from highest to lowest
    middle_orders = sorted(Player.objects.all().filter(batting_position__exact="Middle Order").filter(ODIs_played__gt=80),key = lambda x: -x.get_bat_avg_ODI())
    finisher = sorted(Player.objects.all().filter(batting_position__exact="Finisher").filter(ODIs_played__gt=80),key = lambda x: -x.get_SR_ODI())
    batting_allrounder = sorted(Player.objects.all().filter(Role__exact="Batting Allrounder").filter(ODIs_played__gt=80),key = lambda x: -x.get_bat_avg_ODI())
    bowling_allrounder = sorted(Player.objects.all().filter(Role__exact="Bowling Allrounder").filter(ODIs_played__gt=80),key = lambda x: x.get_economy_ODI())
    fast_bowlers = sorted(Player.objects.all().filter(Role__exact="Fast Bowler").filter(ODIs_played__gt=80),key = lambda x: x.get_bowl_avgODI())
    spin_bowlers = sorted(Player.objects.all().filter(Role__exact="Spin Bowler").filter(ODIs_played__gt=80),key = lambda x: x.get_bowl_avgODI())
    selected_openers = []
    selected_middle_order = []
    selected_finishers = []
    selected_batting_allrounder = batting_allrounder[0]
    selected_bowling_allrounder = bowling_allrounder[0]
    selected_fast_bowlers = []
    selected_spin_bowlers = []
    for i in range (0,2):
        selected_openers.append(openers[i])
    for i in range (0,2):
        selected_middle_order.append(middle_orders[i])
    for i in range (0,1):
        selected_finishers.append(finisher[i])
    for i in range(0,3):
        selected_fast_bowlers.append(fast_bowlers[i])
    for i in range (0,1):
        selected_spin_bowlers.append(spin_bowlers[i])
    
    while(selected_batting_allrounder in selected_openers):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)): # ran out of openers to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_openers.append(openers[case1ctr])
        selected_openers.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1


    while(selected_batting_allrounder in selected_middle_order):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(middle_orders)): # ran out of middleorder batsmen to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_middle_order.append(middle_orders[case1ctr])
        selected_middle_order.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_bowling_allrounder in selected_spin_bowlers):
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)): # ran out of spin bowlers to replace, now replace the battingallrounder
            selected_bowling_allrounder = bowling_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_spin_bowlers.append(spin_bowlers[case1ctr])
        selected_spin_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_spin_bowlers in selected_fast_bowlers):
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            selected_bowling_allrounder = bowling_allrounder[case2ctr];
            case2ctr = case2ctr + 1
        selected_fast_bowlers.append(fast_bowlers[case1ctr])
        selected_fast_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1

    selected_bowlers = (selected_spin_bowlers + selected_fast_bowlers)
    
    context = {}
    context['openers'] = selected_openers
    context['middle_order'] = selected_middle_order
    context['finisher'] = selected_finishers
    context['batting_allrounder'] = selected_batting_allrounder
    context['bowling_allrounder'] = selected_bowling_allrounder
    # context['fast_bowlers'] = selected_fast_bowlers
    # context['spin_bowlers'] = selected_spin_bowlers
    context['bowlers'] = selected_bowlers
    return render(request,'bestXIs/worldXI.html',context)


def worldTestXI(request):
    model = Player
    # getting the best openers
    openers = sorted(Player.objects.all().filter(batting_position__exact="Opener").filter(Tests_played__gt=50),key = lambda x: -x.get_bat_avg_Test()) # the negative sign before x.get_bat_avg_ODI is for sorting from highest to lowest
    middle_orders = sorted(Player.objects.all().filter(batting_position__exact="Middle Order").filter(Tests_played__gt=50),key = lambda x: -x.get_bat_avg_Test())
    finisher = sorted(Player.objects.all().filter(batting_position__exact="Finisher").filter(Tests_played__gt=50),key = lambda x: -x.get_bat_avg_Test())
    batting_allrounder = sorted(Player.objects.all().filter(Role__exact="Batting Allrounder").filter(Tests_played__gt=50),key = lambda x: -x.get_bat_avg_Test())
    bowling_allrounder = sorted(Player.objects.all().filter(Role__exact="Bowling Allrounder").filter(Tests_played__gt=50),key = lambda x: x.get_bowl_avgTest())
    fast_bowlers = sorted(Player.objects.all().filter(Role__exact="Fast Bowler").filter(Tests_played__gt=50),key = lambda x: x.get_bowl_avgTest())
    spin_bowlers = sorted(Player.objects.all().filter(Role__exact="Spin Bowler").filter(Tests_played__gt=50),key = lambda x: x.get_bowl_avgTest())
    selected_openers = []
    selected_middle_order = []
    selected_finishers = []
    selected_batting_allrounder = batting_allrounder[0]
    selected_bowling_allrounder = bowling_allrounder[0]
    selected_fast_bowlers = []
    selected_spin_bowlers = []
    for i in range (0,2):
        selected_openers.append(openers[i])
    for i in range (0,2):
        selected_middle_order.append(middle_orders[i])
    for i in range (0,1):
        selected_finishers.append(finisher[i])
    for i in range(0,3):
        selected_fast_bowlers.append(fast_bowlers[i])
    for i in range (0,1):
        selected_spin_bowlers.append(spin_bowlers[i])

    while(selected_batting_allrounder in selected_openers):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)): # ran out of openers to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_openers.append(openers[case1ctr])
        selected_openers.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1


    while(selected_batting_allrounder in selected_middle_order):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(middle_orders)): # ran out of middleorder batsmen to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_middle_order.append(middle_orders[case1ctr])
        selected_middle_order.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_bowling_allrounder in selected_spin_bowlers):
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)): # ran out of spin bowlers to replace, now replace the battingallrounder
            selected_bowling_allrounder = bowling_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_spin_bowlers.append(spin_bowlers[case1ctr])
        selected_spin_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_spin_bowlers in selected_fast_bowlers):
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            selected_bowling_allrounder = bowling_allrounder[case2ctr];
            case2ctr = case2ctr + 1
        selected_fast_bowlers.append(fast_bowlers[case1ctr])
        selected_fast_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1

    selected_bowlers = selected_spin_bowlers + selected_fast_bowlers
    
    context = {}
    context['openers'] = selected_openers
    context['middle_order'] = selected_middle_order
    context['finisher'] = selected_finishers
    context['batting_allrounder'] = selected_batting_allrounder
    context['bowling_allrounder'] = selected_bowling_allrounder
    # context['fast_bowlers'] = selected_fast_bowlers
    # context['spin_bowlers'] = selected_spin_bowlers
    context['bowlers'] = selected_bowlers
    return render(request,'bestXIs/worldXI.html',context)


def worldT20XI(request):
    model = Player
    # getting the best openers
    openers = sorted(Player.objects.all().filter(batting_position__exact="Opener").filter(T20s_played__gt=30),key = lambda x: -x.get_SR_T20()) # the negative sign before x.get_bat_avg_ODI is for sorting from highest to lowest
    middle_orders = sorted(Player.objects.all().filter(batting_position__exact="Middle Order").filter(T20s_played__gt=30),key = lambda x: -x.get_bat_avg_T20())
    finisher = sorted(Player.objects.all().filter(batting_position__exact="Finisher").filter(T20s_played__gt=30),key = lambda x: -x.get_bat_avg_T20())
    batting_allrounder = sorted(Player.objects.all().filter(Role__exact="Batting Allrounder").filter(T20s_played__gt=30),key = lambda x: -x.get_SR_T20())
    bowling_allrounder = sorted(Player.objects.all().filter(Role__exact="Bowling Allrounder").filter(T20s_played__gt=30),key = lambda x: x.get_economy_T20())
    fast_bowlers = sorted(Player.objects.all().filter(Role__exact="Fast Bowler").filter(T20s_played__gt=30),key = lambda x: x.get_bowl_avgT20())
    spin_bowlers = sorted(Player.objects.all().filter(Role__exact="Spin Bowler").filter(T20s_played__gt=30),key = lambda x: x.get_bowl_avgT20())
    selected_openers = []
    selected_middle_order = []
    selected_finishers = []
    selected_batting_allrounder = batting_allrounder[0]
    selected_bowling_allrounder = bowling_allrounder[0]
    selected_fast_bowlers = []
    selected_spin_bowlers = []
    for i in range (0,2):
        selected_openers.append(openers[i])
    for i in range (0,2):
        selected_middle_order.append(middle_orders[i])
    for i in range (0,1):
        selected_finishers.append(finisher[i])
    for i in range(0,3):
        selected_fast_bowlers.append(fast_bowlers[i])
    for i in range (0,1):
        selected_spin_bowlers.append(spin_bowlers[i])

    while(selected_batting_allrounder in selected_openers):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)): # ran out of openers to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_openers.append(openers[case1ctr])
        selected_openers.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1


    while(selected_batting_allrounder in selected_middle_order):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(middle_orders)): # ran out of middleorder batsmen to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_middle_order.append(middle_orders[case1ctr])
        selected_middle_order.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_bowling_allrounder in selected_spin_bowlers):
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)): # ran out of spin bowlers to replace, now replace the battingallrounder
            selected_bowling_allrounder = bowling_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_spin_bowlers.append(spin_bowlers[case1ctr])
        selected_spin_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_spin_bowlers in selected_fast_bowlers):
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            selected_bowling_allrounder = bowling_allrounder[case2ctr];
            case2ctr = case2ctr + 1
        selected_fast_bowlers.append(fast_bowlers[case1ctr])
        selected_fast_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1

    
    selected_bowlers = selected_spin_bowlers + selected_fast_bowlers
    
    context = {}
    context['openers'] = selected_openers
    context['middle_order'] = selected_middle_order
    context['finisher'] = selected_finishers
    context['batting_allrounder'] = selected_batting_allrounder
    context['bowling_allrounder'] = selected_bowling_allrounder
    context['bowlers'] = selected_bowlers
    return render(request,'bestXIs/worldXI.html',context)


def IPLXI(request):
    model = Player
    # getting the best openers
    openers = sorted(Player.objects.all().filter(batting_position__exact="Opener").filter(IPLs_played__gt=30),key = lambda x: -x.get_SR_IPL()) # the negative sign before x.get_bat_avg_ODI is for sorting from highest to lowest
    middle_orders = sorted(Player.objects.all().filter(batting_position__exact="Middle Order").filter(IPLs_played__gt=30),key = lambda x: -x.get_bat_avg_IPL())
    finisher = sorted(Player.objects.all().filter(batting_position__exact="Finisher").filter(IPLs_played__gt=30),key = lambda x: -x.get_bat_avg_IPL())
    batting_allrounder = sorted(Player.objects.all().filter(Role__exact="Batting Allrounder").filter(IPLs_played__gt=30),key = lambda x: -x.get_SR_IPL())
    bowling_allrounder = sorted(Player.objects.all().filter(Role__exact="Bowling Allrounder").filter(IPLs_played__gt=30),key = lambda x: x.get_economy_IPL())
    fast_bowlers = sorted(Player.objects.all().filter(Role__exact="Fast Bowler").filter(IPLs_played__gt=30),key = lambda x: x.get_bowl_avgIPL())
    spin_bowlers = sorted(Player.objects.all().filter(Role__exact="Spin Bowler").filter(IPLs_played__gt=30),key = lambda x: x.get_bowl_avgIPL())
    selected_openers = []
    selected_middle_order = []
    selected_finishers = []
    selected_batting_allrounder = batting_allrounder[0]
    selected_bowling_allrounder = bowling_allrounder[0]
    selected_fast_bowlers = []
    selected_spin_bowlers = []
    for i in range (0,2):
        selected_openers.append(openers[i])
    for i in range (0,2):
        selected_middle_order.append(middle_orders[i])
    for i in range (0,1):
        selected_finishers.append(finisher[i])
    for i in range(0,3):
        selected_fast_bowlers.append(fast_bowlers[i])
    for i in range (0,1):
        selected_spin_bowlers.append(spin_bowlers[i])
    

    while(selected_batting_allrounder in selected_openers):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)): # ran out of openers to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_openers.append(openers[case1ctr])
        selected_openers.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1


    while(selected_batting_allrounder in selected_middle_order):
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(middle_orders)): # ran out of middleorder batsmen to replace, now replace the battingallrounder
            selected_batting_allrounder = batting_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_middle_order.append(middle_orders[case1ctr])
        selected_middle_order.remove(selected_batting_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_bowling_allrounder in selected_spin_bowlers):
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)): # ran out of spin bowlers to replace, now replace the battingallrounder
            selected_bowling_allrounder = bowling_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_spin_bowlers.append(spin_bowlers[case1ctr])
        selected_spin_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1
    
    while(selected_spin_bowlers in selected_fast_bowlers):
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            selected_bowling_allrounder = bowling_allrounder[case2ctr]
            case2ctr = case2ctr + 1
        selected_fast_bowlers.append(fast_bowlers[case1ctr])
        selected_fast_bowlers.remove(selected_bowling_allrounder)
        case1ctr = case1ctr + 1
    selected_bowlers = selected_spin_bowlers + selected_fast_bowlers
    
    context = {}
    context['openers'] = selected_openers
    context['middle_order'] = selected_middle_order
    context['finisher'] = selected_finishers
    context['batting_allrounder'] = selected_batting_allrounder
    context['bowling_allrounder'] = selected_bowling_allrounder
    context['bowlers'] = selected_bowlers
    return render(request,'bestXIs/worldXI.html',context)

@login_required
def ODITeamX1(request,pk:int):
    model = INTLTeam,Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    team = INTLTeam.objects.get(pk = pk)
    openers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Opener").filter(ODIs_played__gt=0),key=lambda x: -x.get_bat_avg_ODI())
    Middle_Order = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Middle Order").filter(ODIs_played__gt=0),key=lambda x: -x.get_bat_avg_ODI())
    Finishers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Finisher"),key=lambda x: -x.get_bat_avg_ODI())
    Batting_Allrounders = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Batting Allrounder").filter(ODIs_played__gt=0),key=lambda x: -x.get_bat_avg_ODI())
    Bowling_Allrounders = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Bowling Allrounder").filter(ODIs_played__gt=0),key=lambda x: x.get_economy_ODI())
    spin_bowlers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Spin Bowler").filter(ODIs_played__gt=0),key=lambda x: x.get_bowl_avgODI())
    fast_bowlers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Fast Bowler").filter(ODIs_played__gt=0),key=lambda x: x.get_bowl_avgODI())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
                break
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(Middle_Order[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
                break
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
                break
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
                break
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    context['team'] = team
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)
    
    # for i in range(0,len(openers)):
    #     selectedopeners.append(openers[i])
        
    # for i in range(0,len(Middle_Order)):
    #     selectedmiddleorder.append(Middle_Order[i])
        
    # for i in range(0,len(Finishers)):
    #     selectedfinisher.append(Finishers[i])
        
    # for i in range(0,len(Batting_Allrounders)):
    #     selectedbattingallrounder.append(Batting_Allrounders[i])
        
    # for i in range(0,len(Bowling_Allrounders)):
    #     selectedbowlingallrounder.append(Bowling_Allrounders[i])
        
    # for i in range(0,len(spin_bowlers)):
    #     selectedspinbowlers.append(spin_bowlers[i])
        
    # for i in range(0,len(fast_bowlers)):
    #     selectedfastbowlers.append(fast_bowlers[i])
    
    # final_team = selectedopeners + selectedmiddleorder + selectedfinisher + selectedbattingallrounder + selectedbowlingallrounder + selectedspinbowlers + selectedfastbowlers
    # res = True
    # if len(final_team) < 11:
    #     res = False
    # # if len(selectedopeners) >2 or len(selectedmiddleorder) >2 or selectedfinisher.le:
    # #     print("")
        


    # return HttpResponse("hey there aren't enough players mfk")
@login_required
def TestTeamX1(request,pk:int):
    model = INTLTeam,Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    team = INTLTeam.objects.get(pk = pk)
    openers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Opener").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Middle_Order = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Middle Order").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Finishers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Finisher").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Batting_Allrounders = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Batting Allrounder").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Bowling_Allrounders = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Bowling Allrounder").filter(Tests_played__gt=0),key=lambda x: x.get_bowl_avgTest())
    spin_bowlers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Spin Bowler").filter(Tests_played__gt=0),key=lambda x: x.get_bowl_avgTest())
    fast_bowlers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Fast Bowler").filter(Tests_played__gt=0),key=lambda x: x.get_bowl_avgTest())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(Middle_Order[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    context['team'] = team
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)
@login_required
def T20TeamX1(request,pk:int):
    model = INTLTeam,Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    team = INTLTeam.objects.get(pk = pk)
    openers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Opener").filter(T20s_played__gt=0),key=lambda x: -x.get_SR_T20())
    Middle_Order = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Middle Order").filter(T20s_played__gt=0),key=lambda x: -x.get_bat_avg_T20())
    Finishers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(batting_position__exact="Finisher").filter(T20s_played__gt=0),key=lambda x: -x.get_bat_avg_T20())
    Batting_Allrounders = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Batting Allrounder").filter(T20s_played__gt=0),key=lambda x: -x.get_SR_T20())
    Bowling_Allrounders = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Bowling Allrounder").filter(T20s_played__gt=0),key=lambda x: x.get_economy_T20())
    spin_bowlers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Spin Bowler").filter(T20s_played__gt=0),key=lambda x: x.get_bowl_avgT20())
    fast_bowlers = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Fast Bowler").filter(T20s_played__gt=0),key=lambda x: x.get_bowl_avgT20())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(openers[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    context['team'] = team
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    context['heading'] = "This is my Personal Team T2O X1"
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)

def IPLTeamX1(request,pk:int):
    model = IPLTeam,Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    team = IPLTeam.objects.get(pk = pk)
    openers = sorted(Player.objects.all().filter(iplteam__pk__exact=team.pk).filter(batting_position__exact="Opener").filter(IPLs_played__gt=0),key=lambda x: -x.get_SR_IPL())
    Middle_Order = sorted(Player.objects.all().filter(iplteam__pk__exact=team.pk).filter(batting_position__exact="Middle Order").filter(IPLs_played__gt=0),key=lambda x: -x.get_bat_avg_IPL())
    Finishers = sorted(Player.objects.all().filter(iplteam__pk__exact=team.pk).filter(batting_position__exact="Finisher").filter(IPLs_played__gt=0),key=lambda x: -x.get_bat_avg_IPL())
    Batting_Allrounders = sorted(Player.objects.all().filter(intlteam__pk__exact=team.pk).filter(Role__exact="Batting Allrounder").filter(IPLs_played__gt=0),key=lambda x: -x.get_SR_IPL())
    Bowling_Allrounders = sorted(Player.objects.all().filter(iplteam__pk__exact=team.pk).filter(Role__exact="Bowling Allrounder").filter(IPLs_played__gt=0),key=lambda x: x.get_economy_IPL())
    spin_bowlers = sorted(Player.objects.all().filter(iplteam__pk__exact=team.pk).filter(Role__exact="Spin Bowler").filter(IPLs_played__gt=0),key=lambda x: x.get_bowl_avgIPL())
    fast_bowlers = sorted(Player.objects.all().filter(iplteam__pk__exact=team.pk).filter(Role__exact="Fast Bowler").filter(IPLs_played__gt=0),key=lambda x: x.get_bowl_avgIPL())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(openers[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    context['team'] = team
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)

@login_required
def MyT20TeamX1(request):
    model = Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    # team = INTLTeam.objects.get()
    openers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Opener").filter(T20s_played__gt=0),key=lambda x: -x.get_SR_T20())
    Middle_Order = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Middle Order").filter(T20s_played__gt=0),key=lambda x: -x.get_bat_avg_T20())
    Finishers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Finisher").filter(T20s_played__gt=0),key=lambda x: -x.get_bat_avg_T20())
    Batting_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Batting Allrounder").filter(T20s_played__gt=0),key=lambda x: -x.get_SR_T20())
    Bowling_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Bowling Allrounder").filter(T20s_played__gt=0),key=lambda x: x.get_economy_T20())
    spin_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Spin Bowler").filter(T20s_played__gt=0),key=lambda x: x.get_bowl_avgT20())
    fast_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Fast Bowler").filter(T20s_played__gt=0),key=lambda x: x.get_bowl_avgT20())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(openers[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    context['heading'] = "This is my Personal T20 XI"
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)


def MYIPLTeamX1(request):
    model = IPLTeam,Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    # team = IPLTeam.objects.get(pk = pk)
    openers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Opener").filter(IPLs_played__gt=0),key=lambda x: -x.get_SR_IPL())
    Middle_Order = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Middle Order").filter(IPLs_played__gt=0),key=lambda x: -x.get_bat_avg_IPL())
    Finishers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Finisher").filter(IPLs_played__gt=0),key=lambda x: -x.get_bat_avg_IPL())
    Batting_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Batting Allrounder").filter(IPLs_played__gt=0),key=lambda x: -x.get_SR_IPL())
    Bowling_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Bowling Allrounder").filter(IPLs_played__gt=0),key=lambda x: x.get_economy_IPL())
    spin_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Spin Bowler").filter(IPLs_played__gt=0),key=lambda x: x.get_bowl_avgIPL())
    fast_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Fast Bowler").filter(IPLs_played__gt=0),key=lambda x: x.get_bowl_avgIPL())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(openers[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    # context['team'] = team
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    context['heading'] = "This is my Personal IPL XI"
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)


@login_required
def MyTestTeamX1(request):
    model = INTLTeam,Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    # team = INTLTeam.objects.get(pk = pk)
    openers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Opener").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Middle_Order = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Middle Order").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Finishers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Finisher").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Batting_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Batting Allrounder").filter(Tests_played__gt=0),key=lambda x: -x.get_bat_avg_Test())
    Bowling_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Bowling Allrounder").filter(Tests_played__gt=0),key=lambda x: x.get_bowl_avgTest())
    spin_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Spin Bowler").filter(Tests_played__gt=0),key=lambda x: x.get_bowl_avgTest())
    fast_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Fast Bowler").filter(Tests_played__gt=0),key=lambda x: x.get_bowl_avgTest())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(Middle_Order[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    # context['team'] = team
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    context['heading'] = "This is my Persoal Test XI"
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)


@login_required
def MyODITeamX1(request):
    model = INTLTeam,Player
    context = {}
    # context['team'] = INTLTeam.objects.get(pk=pk)
    # context['players'] = Player.objects.all()
    # team = INTLTeam.objects.get(pk = pk)
    openers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Opener").filter(ODIs_played__gt=0),key=lambda x: -x.get_bat_avg_ODI())
    Middle_Order = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Middle Order").filter(ODIs_played__gt=0),key=lambda x: -x.get_bat_avg_ODI())
    Finishers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(batting_position__exact="Finisher"),key=lambda x: -x.get_bat_avg_ODI())
    Batting_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Batting Allrounder").filter(ODIs_played__gt=0),key=lambda x: -x.get_bat_avg_ODI())
    Bowling_Allrounders = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Bowling Allrounder").filter(ODIs_played__gt=0),key=lambda x: x.get_economy_ODI())
    spin_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Spin Bowler").filter(ODIs_played__gt=0),key=lambda x: x.get_bowl_avgODI())
    fast_bowlers = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Role__exact="Fast Bowler").filter(ODIs_played__gt=0),key=lambda x: x.get_bowl_avgODI())
    
    selectedopeners = []
    selectedmiddleorder = []
    selectedfinisher = []
    selectedbattingallrounder = []
    selectedbowlingallrounder = []
    selectedspinbowlers = []
    selectedfastbowlers = []
    
    result1 = False
    result2 = False
    result3 = False
    result4 = False
    result5 = False
    result6 = False
    result7 = False
    if len(openers) < 2:
        result1 = True
        context['result1'] = result1
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Middle_Order) < 2:
        result2 = True
        context['result2'] = result2
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Finishers) < 1:
        result3 = True
        context['result3'] = result3
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Batting_Allrounders) < 1:
        result4 = True
        context['result4'] = result4
        return render(request,'bestXIs/TeamX1.html',context)
    if len(Bowling_Allrounders) < 1:
        result5 = True
        context['result5'] = result5
        return render(request,'bestXIs/TeamX1.html',context)
    if len(fast_bowlers) < 3:
        result6 = True
        context['result6'] = result6
        return render(request,'bestXIs/TeamX1.html',context)
    if len(spin_bowlers) < 1:
        result7 = True
        context['result7'] = result7
        return render(request,'bestXIs/TeamX1.html',context)


    for i in range(0,2):
        selectedopeners.append(openers[i])
    for i in range(0,2):
        selectedmiddleorder.append(Middle_Order[i])
    for i in range(0,1):
        selectedfinisher.append(Finishers[i])

    selectedbattingallrounder = Batting_Allrounders[0]
    selectedbowlingallrounder = Bowling_Allrounders[0]

    for i in range(0,3):
        selectedfastbowlers.append(fast_bowlers[i])
    for i in range(0,1):
        selectedspinbowlers.append(spin_bowlers[i])
    
    res1 = False
    res2 = False
    res3 = False
    res4 = False
    res5 = False

    while selectedbattingallrounder in selectedopeners:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(openers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res1 = True
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedopeners.append(openers[case1ctr])
        selectedopeners.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1
        
    while selectedbattingallrounder in selectedmiddleorder:
        case1ctr = 2
        case2ctr = 1
        if(case1ctr >= len(Middle_Order)):
            if(case2ctr >= len(Batting_Allrounders)):
                res2 = True
                break
            selectedbattingallrounder = Batting_Allrounders[case2ctr]
            case2ctr = case2ctr + 1
        selectedmiddleorder.append(Middle_Order[case1ctr])
        selectedmiddleorder.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbattingallrounder in selectedfinisher:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(Finishers)):
            if(case2ctr >= len(Batting_Allrounders)):
                res5 = True
                break
            selectedbattingallrounder = Finishers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfinisher.append(Finishers[case1ctr])
        selectedfinisher.remove(selectedbattingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedfastbowlers:
        case1ctr = 3
        case2ctr = 1
        if(case1ctr >= len(fast_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res3 = True
                break
            selectedbowlingallrounder = fast_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedfastbowlers.append(fast_bowlers[case1ctr])
        selectedfastbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1

    while selectedbowlingallrounder in selectedspinbowlers:
        case1ctr = 1
        case2ctr = 1
        if(case1ctr >= len(spin_bowlers)):
            if(case2ctr >= len(Bowling_Allrounders)):
                res4 = True
                break
            selectedbowlingallrounder = spin_bowlers[case2ctr]
            case2ctr = case2ctr + 1
        selectedspinbowlers.append(spin_bowlers[case1ctr])
        selectedspinbowlers.remove(selectedbowlingallrounder)
        case1ctr = case1ctr + 1
    
    

    # context['result1'] = result1
    # context['result2'] = result2
    # context['result3'] = result3
    # context['result4'] = result4
    # context['result5'] = result5
    # context['result6'] = result6
    # context['result7'] = result7
    context['res1'] = res1
    context['res2'] = res2
    context['res3'] = res3
    context['res4'] = res4
    context['res5'] = res5
    context['openers'] = selectedopeners
    context['Middle_Order'] = selectedmiddleorder
    context['Finisher'] = selectedfinisher
    context['Batting_Allrounder'] = selectedbattingallrounder
    context['Bowling_Allrounder'] = selectedbowlingallrounder
    context['Spin_Bowler'] = selectedspinbowlers
    context['Fast_Bowler'] = selectedfastbowlers
    context['heading'] = "This is my Personal ODI XI"
    # context['result'] = res

    return render(request,'bestXIs/TeamX1.html',context)

def ViewStats(request):
    all_batsmen_ODI = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_ODI())
    all_batsmen_Test = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_Test())
    all_batsmen_IPL = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_IPL())
    all_batsmen_T20 = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_T20())
    
    all_batsmen_ODI_SR = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_ODI())
    all_batsmen_Test_SR = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_Test())
    all_batsmen_IPL_SR = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_IPL())
    all_batsmen_T20_SR = sorted(Player.objects.all().filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_T20())
    
    all_bowler_ODI_eco = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_ODI__gt=20),key = lambda x: x.get_economy_ODI())
    all_bowler_Test_eco = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_Test__gt=20),key = lambda x: x.get_economy_Test())
    all_bowler_IPL_eco = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_IPL__gt=20),key = lambda x: x.get_economy_IPL())
    all_bowler_T20_eco = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_T20__gt=20),key = lambda x: x.get_economy_T20())
    
    all_bowler_ODI_bowl_avg = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_ODI__gt=20),key = lambda x: x.get_bowl_avgODI())
    all_bowler_Test_bowl_avg = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_Test__gt=20),key = lambda x: x.get_bowl_avgTest())
    all_bowler_IPL_bowl_avg = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_IPL__gt=20),key = lambda x: x.get_bowl_avgIPL())
    all_bowler_T20_bowl_avg = sorted(Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_T20__gt=20),key = lambda x: x.get_bowl_avgT20())

    all_wickets_ODI = Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).order_by('-wicketsODI')
    all_wickets_Test = Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).order_by('-wicketsTest')
    all_wickets_T20 = Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).order_by('-wicketsIPL')
    all_wickets_IPL = Player.objects.all().filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).order_by('-wicketsT20')

    batsmen_ODI_avg = []
    batsmen_Test_avg = []
    batsmen_IPL_avg = []
    batsmen_T20_avg = []

    batsmen_ODI_SR = []
    batsmen_Test_SR = []
    batsmen_IPL_SR = []
    batsmen_T20_SR = []

    bowlers_ODI_eco = []
    bowlers_Test_eco = []
    bowlers_IPL_eco = []
    bowlers_T20_eco = []

    bowlers_ODI_bowl_avg = []
    bowlers_Test_bowl_avg = []
    bowlers_IPL_bowl_avg = []
    bowlers_T20_bowl_avg = []

    wicketsODI = []
    wicketsTest = []
    wicketsIPL = []
    wicketsT20 = []

    if len(all_batsmen_ODI) > 10:
        for i in range(0,10):
            batsmen_ODI_avg.append(all_batsmen_ODI[i])
    if len(all_batsmen_Test) > 10:
        for i in range(0,10):
            batsmen_Test_avg.append(all_batsmen_Test[i])
    if len(all_batsmen_IPL) > 10:
        for i in range(0,10):
            batsmen_IPL_avg.append(all_batsmen_IPL[i])
    if len(all_batsmen_T20) > 10:
        for i in range(0,10):
            batsmen_T20_avg.append(all_batsmen_T20[i])

    SR_ctr = 0
    while SR_ctr < len(all_batsmen_ODI_SR):
        batsmen_ODI_SR.append(all_batsmen_ODI_SR[SR_ctr])
        if SR_ctr == 10:
            break
        SR_ctr = SR_ctr + 1
    SR_ctr = 0
    SR_ctr = 0
    while SR_ctr < len(all_batsmen_Test_SR):
        batsmen_Test_SR.append(all_batsmen_Test_SR[SR_ctr])
        if SR_ctr == 10:
            break
        SR_ctr = SR_ctr + 1
    SR_ctr = 0
    while SR_ctr < len(all_batsmen_IPL_SR):
        batsmen_IPL_SR.append(all_batsmen_IPL_SR[SR_ctr])
        if SR_ctr == 10:
            break
        SR_ctr = SR_ctr + 1
    SR_ctr = 0
    while SR_ctr < len(all_batsmen_T20_SR):
        batsmen_T20_SR.append(all_batsmen_T20_SR[SR_ctr])
        if SR_ctr == 10:
            break
        SR_ctr = SR_ctr + 1
    SR_ctr = 0

    eco_ctr = 0
    while eco_ctr < len(all_bowler_ODI_eco):
        bowlers_ODI_eco.append(all_bowler_ODI_eco[eco_ctr])
        if eco_ctr == 10:
            break
        eco_ctr = eco_ctr + 1
    eco_ctr = 0
    while eco_ctr < len(all_bowler_Test_eco):
        bowlers_Test_eco.append(all_bowler_Test_eco[eco_ctr])
        if eco_ctr == 10:
            break
        eco_ctr = eco_ctr + 1
    eco_ctr = 0
    while eco_ctr < len(all_bowler_IPL_eco):
        bowlers_IPL_eco.append(all_bowler_IPL_eco[eco_ctr])
        if eco_ctr == 10:
            break
        eco_ctr = eco_ctr + 1
    eco_ctr = 0
    while eco_ctr < len(all_bowler_T20_eco):
        bowlers_T20_eco.append(all_bowler_T20_eco[eco_ctr])
        if eco_ctr == 10:
            break
        eco_ctr = eco_ctr + 1
    eco_ctr = 0
        
    bowl_avg_ctr = 0
    while bowl_avg_ctr < len(all_bowler_ODI_bowl_avg):
        bowlers_ODI_bowl_avg.append(all_bowler_ODI_bowl_avg[bowl_avg_ctr])
        if bowl_avg_ctr == 10:
            break
        bowl_avg_ctr = bowl_avg_ctr + 1
    bowl_avg_ctr = 0
    while bowl_avg_ctr < len(all_bowler_Test_bowl_avg):
        bowlers_Test_bowl_avg.append(all_bowler_Test_bowl_avg[bowl_avg_ctr])
        if bowl_avg_ctr == 10:
            break
        bowl_avg_ctr = bowl_avg_ctr + 1
    bowl_avg_ctr = 0
    while bowl_avg_ctr < len(all_bowler_IPL_bowl_avg):
        bowlers_IPL_bowl_avg.append(all_bowler_IPL_bowl_avg[bowl_avg_ctr])
        if bowl_avg_ctr == 10:
            break
        bowl_avg_ctr = bowl_avg_ctr + 1
    bowl_avg_ctr = 0
    while bowl_avg_ctr < len(all_bowler_T20_bowl_avg):
        bowlers_T20_bowl_avg.append(all_bowler_T20_bowl_avg[bowl_avg_ctr])
        if bowl_avg_ctr == 10:
            break
        bowl_avg_ctr = bowl_avg_ctr + 1
    bowl_avg_ctr = 0

    wickets_ctr = 0
    while wickets_ctr < len(all_wickets_ODI):
        wicketsODI.append(all_wickets_ODI[wickets_ctr])
        if wickets_ctr == 10:
            break
        wickets_ctr = wickets_ctr + 1
    wickets_ctr = 0

    while wickets_ctr < len(all_wickets_Test):
        wicketsTest.append(all_wickets_Test[wickets_ctr])
        if wickets_ctr == 10:
            break
        wickets_ctr = wickets_ctr + 1
    wickets_ctr = 0

    while wickets_ctr < len(all_wickets_IPL):
        wicketsIPL.append(all_wickets_IPL[wickets_ctr])
        if wickets_ctr == 10:
            break
        wickets_ctr = wickets_ctr + 1
    wickets_ctr = 0

    while wickets_ctr < len(all_wickets_T20):
        wicketsT20.append(all_wickets_T20[wickets_ctr])
        if wickets_ctr == 10:
            break
        wickets_ctr = wickets_ctr + 1
    wickets_ctr = 0

    context = {}
    context['ODI_bat_avg_batsmen'] = batsmen_ODI_avg
    context['Test_bat_avg_batsmen'] = batsmen_Test_avg
    context['IPL_bat_avg_batsmen'] = batsmen_IPL_avg
    context['T20_bat_avg_batsmen'] = batsmen_T20_avg
    context['ODI_SR_batsmen'] = batsmen_ODI_SR
    context['Test_SR_batsmen'] = batsmen_Test_SR
    context['T20_SR_batsmen'] = batsmen_T20_SR
    context['IPL_SR_batsmen'] = batsmen_IPL_SR
    context['ODI_eco_bowlers'] = bowlers_ODI_eco
    context['Test_eco_bowlers'] = bowlers_Test_eco
    context['IPL_eco_bowlers'] = bowlers_IPL_eco
    context['T20_eco_bowlers'] = bowlers_T20_eco
    context['ODI_bowl_avg'] = bowlers_ODI_bowl_avg
    context['Test_bowl_avg'] = bowlers_Test_bowl_avg
    context['IPL_bowl_avg'] = bowlers_IPL_bowl_avg
    context['T20_bowl_avg'] = bowlers_T20_bowl_avg
    context['wickets_ODI'] = wicketsODI
    context['wickets_Test'] = wicketsTest
    context['wickets_IPL'] = wicketsIPL
    context['wickets_T20'] = wicketsT20
    # openers = sorted(Player.objects.all().filter(batting_position__exact="Opener").filter(ODIs_played__gt=80),key = lambda x: -x.get_bat_avg_ODI())
    return render(request,'graphs/allplayerstats.html',context)

@login_required
def viewuserStats(request):
    all_batsmen_ODI = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(ODIs_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_ODI())
    all_batsmen_Test = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Tests_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_Test())
    all_batsmen_IPL = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(IPLs_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_IPL())
    all_batsmen_T20 = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(T20s_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_bat_avg_T20())
    all_batsmen_ODI_SR = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(ODIs_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_ODI())
    all_batsmen_Test_SR = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Tests_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_Test())
    all_batsmen_IPL_SR = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(IPLs_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_IPL())
    all_batsmen_T20_SR = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(T20s_played__gt=0).filter(Q(Role__exact="Batsman") | Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder")),key = lambda x: -x.get_SR_T20())
    all_bowler_ODI_eco = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_ODI__gt=20),key = lambda x: x.get_economy_ODI())
    all_bowler_Test_eco = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_Test__gt=20),key = lambda x: x.get_economy_Test())
    all_bowler_IPL_eco = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_IPL__gt=20),key = lambda x: x.get_economy_IPL())
    all_bowler_T20_eco = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_T20__gt=20),key = lambda x: x.get_economy_T20())
    # all_bowler_ODI_bowl_avg = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_ODI__gt=20),key = lambda x: x.get_bowl_avgODI())
    # all_bowler_Test_bowl_avg = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_Test__gt=20),key = lambda x: x.get_bowl_avgTest())
    # all_bowler_IPL_bowl_avg = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_IPL__gt=20),key = lambda x: x.get_bowl_avgIPL())
    # all_bowler_T20_bowl_avg = sorted(Player.objects.all().filter(ownerplayer=request.user).filter(Q(Role__exact="Batting Allrounder") | Q(Role__exact="Bowling Allrounder") | Q(Role__exact="Fast Bowler") | Q(Role__exact="Spin Bowler")).filter(innings_bowled_T20__gt=20),key = lambda x: x.get_bowl_avgT20())

    context = {}
    context['ODI_bat_avg_batsmen'] = all_batsmen_ODI
    context['Test_bat_avg_batsmen'] = all_batsmen_Test
    context['IPL_bat_avg_batsmen'] = all_batsmen_IPL
    context['T20_bat_avg_batsmen'] = all_batsmen_T20
    context['all_batsmen_ODI_SR'] = all_batsmen_ODI_SR
    context['all_batsmen_Test_SR'] = all_batsmen_Test_SR
    context['all_batsmen_IPL_SR'] = all_batsmen_IPL_SR
    context['all_batsmen_T20_SR'] = all_batsmen_T20_SR
    context['all_bowler_ODI_eco'] = all_bowler_ODI_eco
    context['all_bowler_Test_eco'] = all_bowler_Test_eco
    context['all_bowler_IPL_eco'] = all_bowler_IPL_eco
    context['all_bowler_T20_eco'] = all_bowler_T20_eco
    # context['all_bowler_ODI_bowl_avg'] = all_bowler_ODI_bowl_avg
    # context['all_bowler_Test_bowl_avg'] = all_bowler_Test_bowl_avg
    # context['all_bowler_IPL_bowl_avg'] = all_bowler_IPL_bowl_avg
    # context['all_bowler_T20_bowl_avg'] = all_bowler_T20_bowl_avg
    return render(request,'graphs/myplayerstats.html',context)
