# Generated by Django 4.1.5 on 2023-04-23 06:36

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='INTLTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('flagintl', models.ImageField(default=0, upload_to='intl')),
                ('World_cups_won', models.IntegerField()),
                ('Champion_trophies_won', models.IntegerField()),
                ('T20WC_trophies_won', models.IntegerField()),
                ('Asia_Cups_Won', models.IntegerField()),
                ('ODI_matches_played', models.IntegerField()),
                ('Test_matches_played', models.IntegerField()),
                ('T20_matches_played', models.IntegerField()),
                ('ownerINTL', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_ownerINTL', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IPLTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('flagipl', models.ImageField(default=0, upload_to='ipl')),
                ('matches_played', models.IntegerField(default=0)),
                ('matches_won', models.IntegerField(default=0)),
                ('matches_lost', models.IntegerField(default=0)),
                ('trophies_won', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_ownerIPL', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile_extend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(default='user/default.jpg', upload_to='user')),
                ('Twitter', models.URLField(blank=True, default='', max_length=300)),
                ('Facebook', models.URLField(blank=True, default='', max_length=300)),
                ('Instagram', models.URLField(blank=True, default='', max_length=300)),
                ('LinkedIn', models.URLField(blank=True, default='', max_length=300)),
                ('Github', models.URLField(blank=True, default='', max_length=300)),
                ('bio', models.CharField(blank=True, default='', max_length=150)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, default='', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('player_image', models.ImageField(default='players/default.jpg', upload_to='players')),
                ('age', models.IntegerField()),
                ('jersey_number', models.IntegerField(default=0)),
                ('Role', models.CharField(choices=[('Batsman', 'Batsman'), ('Batting Allrounder', 'Batting Allrounder'), ('Bowling Allrounder', 'Bowling Allrounder'), ('Fast Bowler', 'Fast Bowler'), ('Spin Bowler', 'Spin Bowler'), ('cheerleader', 'cheerleader')], default='cheerleader', max_length=25)),
                ('batting_position', models.CharField(choices=[('Opener', 'Opener'), ('Middle Order', 'Middle Order'), ('Finisher', 'Finisher'), ('Tailender', 'Tailender')], default='Tailender', max_length=25)),
                ('ODIs_played', models.IntegerField(default=0)),
                ('ODIs_innings_played', models.IntegerField(default=0)),
                ('highest_scoreODI', models.IntegerField(blank=True, default=0)),
                ('total_runsODI', models.IntegerField(default=0)),
                ('total_balls_facedODI', models.IntegerField(default=0)),
                ('not_outsODI', models.IntegerField(default=0)),
                ('fiftiesODI', models.IntegerField(default=0)),
                ('hundredsODI', models.IntegerField(default=0)),
                ('innings_bowled_ODI', models.IntegerField(default=0)),
                ('total_bowlsODI', models.IntegerField(default=0)),
                ('total_runs_givenODI', models.IntegerField(default=0)),
                ('wicketsODI', models.IntegerField(default=0)),
                ('IPLs_played', models.IntegerField(default=0)),
                ('IPLs_innings_played', models.IntegerField(default=0)),
                ('highest_scoreIPL', models.IntegerField(blank=True, default=0)),
                ('total_runsIPL', models.IntegerField(default=0)),
                ('total_balls_facedIPL', models.IntegerField(default=0)),
                ('not_outsIPL', models.IntegerField(default=0)),
                ('fiftiesIPL', models.IntegerField(default=0)),
                ('hundredsIPL', models.IntegerField(default=0)),
                ('innings_bowled_IPL', models.IntegerField(default=0)),
                ('total_bowlsIPL', models.IntegerField(default=0)),
                ('total_runs_givenIPL', models.IntegerField(default=0)),
                ('wicketsIPL', models.IntegerField(default=0)),
                ('Tests_played', models.IntegerField(default=0)),
                ('Tests_innings_played', models.IntegerField(default=0)),
                ('highest_scoreTest', models.IntegerField(blank=True, default=0)),
                ('total_runsTest', models.IntegerField(default=0)),
                ('total_balls_facedTest', models.IntegerField(default=0)),
                ('not_outsTest', models.IntegerField(default=0)),
                ('fiftiesTest', models.IntegerField(default=0)),
                ('hundredsTest', models.IntegerField(default=0)),
                ('innings_bowled_Test', models.IntegerField(default=0)),
                ('total_bowlsTest', models.IntegerField(default=0)),
                ('total_runs_givenTest', models.IntegerField(default=0)),
                ('wicketsTest', models.IntegerField(default=0)),
                ('T20s_played', models.IntegerField(default=0)),
                ('T20s_innings_played', models.IntegerField(default=0)),
                ('highest_scoreT20', models.IntegerField(blank=True, default=0)),
                ('total_runsT20', models.IntegerField(default=0)),
                ('total_balls_facedT20', models.IntegerField(default=0)),
                ('not_outsT20', models.IntegerField(default=0)),
                ('fiftiesT20', models.IntegerField(default=0)),
                ('hundredsT20', models.IntegerField(default=0)),
                ('innings_bowled_T20', models.IntegerField(default=0)),
                ('total_bowlsT20', models.IntegerField(default=0)),
                ('total_runs_givenT20', models.IntegerField(default=0)),
                ('wicketsT20', models.IntegerField(default=0)),
                ('intlteam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intl_player', to='player.intlteam')),
                ('iplteam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='iplplayer', to='player.iplteam')),
                ('ownerplayer', models.ForeignKey(default=django.contrib.auth.models.User, on_delete=django.db.models.deletion.CASCADE, related_name='rel_ownerplayer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
