import re
import os
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
#import time
#import lxml


boxscore_outfile = open("boxscore_table.csv", "a+", encoding='utf-8')
pitcher_outfile = open("pitcher_table.csv", "a+", encoding='utf-8')
batter_outfile = open("batter_table.csv", "a+", encoding='utf-8')

file_cont = ""
'''while file_cont!="yes" and file_cont!="no":
	file_cont = input("Continue files from previous spot? Type yes/no: ")'''

if file_cont == "yes":
	ll_retroid = boxscore_outfile.readlines()[-1:][0].split(",")[0]
	startdate = datetime.date(int(ll_retroid[0:4]), int(ll_retroid[4:6]), 	 int(ll_retroid[6:8]))+datetime.timedelta(days=1)
else:
	startdate_choice_fl = ""
	while startdate_choice_fl != "yes" and startdate_choice_fl != "no":
		startdate_choice_fl = input("Choose starting date? Type yes or no: ")

	if startdate_choice_fl == "yes":
		start_year = int(input("Starting year: "))
		start_month = int(input("Starting month: "))
		start_day = int(input("Starting day: "))
		startdate = datetime.date(start_year, start_month, start_day)
	else:
		startdate = datetime.date(2008, 1, 1)

enddate_choice_fl = ""
while enddate_choice_fl != "yes" and enddate_choice_fl != "no":
	enddate_choice_fl = input("Choose ending date? Type yes or no: ")

if enddate_choice_fl == "yes":
	end_year = int(input("Ending year: "))
	end_month = int(input("Ending month: "))
	end_date = int(input("Ending day: "))
	enddate = datetime.date(end_year, end_month, end_date)
else:
	enddate = datetime.date.today()-datetime.timedelta(days=1)

if os.stat("boxscore_table.csv").st_size == 0:
	boxscore_outfile.write("game_id,date,game_pk,game_type_des,away_fname,home_fname,away_id,home_id,home_pitcher,away_pitcher,home_lineup,away_lineup,away_team_runs,home_team_runs,home_win,winning_team,home_wins,home_loss,away_wins,away_loss\n")
if os.stat("pitcher_table.csv").st_size == 0:
	pitcher_outfile.write("game_id,date,game_pk,away_fname,home_fname,away_id,home_id,team_flag,total_runs,total_earned_runs,pitcher_id,pitcher_name,p_runs,p_earned_runs,outs,p_so,p_era,win_col,loss_col,wins,losses\n")
if os.stat("batter_table.csv").st_size == 0:
	batter_outfile.write("game_id,date,game_pk,away_fname,home_fname,away_id,home_id,team_flag,total_runs,total_earned_runs,batter_id,batter_name,position,at_bats,hits,runs,strike_out,walk,home_run,double,triple,rbi,stolen_bases,avg,obp,slg,slob\n")

base_url = "http://gd2.mlb.com/components/game/mlb/"

delta = enddate - startdate
prior_d_url = ""

for i in range(delta.days+1):
	active_date = (startdate+datetime.timedelta(days=i))
	print base_url+"year_"+str((startdate+datetime.timedelta(days=i)).year)+"/month_"+active_date.strftime('%m')+"/day_"+active_date.strftime('%d')+"/"
	try:
		urlopen(base_url+"year_"+str((startdate+datetime.timedelta(days=i)).year)+"/month_"+active_date.strftime('%m')+"/day_"+active_date.strftime('%d')+"/")
		d_url = base_url+"year_"+str((startdate+datetime.timedelta(days=i)).year)+"/month_"+active_date.strftime('%m')+"/day_"+active_date.strftime('%d')+"/"
	except:
		print "excepted"
		d_url = prior_d_url
	if d_url != prior_d_url:
		day_soup = BeautifulSoup(urlopen(d_url))
		for game in day_soup.find_all("a", href=re.compile("gid_.*")):
			g = game.get_text().strip()
			if isinstance(game.get_text().strip()[len(game.get_text().strip())-2:len(game.get_text().strip())-1]) == isinstance(int(1)):
				game_number = game.get_text().strip()[len(game.get_text().strip())-2:len(game.get_text().strip())-1]
			else:
				game_number = 1
			g_url = d_url+g
			print g
			if BeautifulSoup(urlopen(g_url), "html.parser").find("a", href="game.xml"):
				detail_soup = BeautifulSoup(urlopen(g_url+"game.xml"), "html.parser")
				if 'type' in detail_soup.game.attrs:
					game_type = detail_soup.game["type"]
				else:
					game_type = "U"
				if game_type == "S":
					game_type_des = "Spring Training"
					st_fl = "T"
				elif game_type == "R":
					game_type_des = "Regular Season"
					regseason_fl = "T"
				elif game_type == "F":
					game_type_des = "Wild-card Game"
					playoff_fl = "T"
				elif game_type == "D":
					game_type_des = "Divisional Series"
					playoff_fl = "T"
				elif game_type == "L":
					game_type_des = "League Championship Series"
					playoff_fl = "T"
				elif game_type == "W":
					game_type_des = "World Series"
					playoff_fl = "T"
				else:
					game_type_des = "Unknown"
			if BeautifulSoup(urlopen(g_url), "html.parser").find("a", href="boxscore.xml"):
				detail_soup = BeautifulSoup(urlopen(g_url+"boxscore.xml"), "html.parser")
				if 'game_id' in detail_soup.boxscore.attrs:
					game_id = detail_soup.boxscore["game_id"]
				else:
					game_id = "unknown"
				if 'game_pk' in detail_soup.boxscore.attrs:
					game_pk = detail_soup.boxscore["game_pk"]
				else:
					game_pk = "unknown"
				if 'away_fname' in detail_soup.boxscore.attrs:
					away_fname = detail_soup.boxscore["away_fname"]
				else:
					away_fname = "unknown"
				if 'home_fname' in detail_soup.boxscore.attrs:
					home_fname = detail_soup.boxscore["home_fname"]
				else:
					home_fname = "unknown"
				if 'home_id' in detail_soup.boxscore.attrs:
					home_id = detail_soup.boxscore["home_id"]
				else:
					home_id = "unknown"
				if 'away_id' in detail_soup.boxscore.attrs:
					away_id = detail_soup.boxscore["away_id"]
				else:
					away_id = "unknown"
				if 'date' in detail_soup.boxscore.attrs:
					date = detail_soup.boxscore["date"]
				else:
					date = "unknown"
				if 'away_wins' in detail_soup.boxscore.attrs:
					away_wins = detail_soup.boxscore["away_wins"]
				else:
					away_wins = "unknown"
				if 'home_wins' in detail_soup.boxscore.attrs:
					home_wins = detail_soup.boxscore["home_wins"]
				else:
					home_wins = "unknown"
				if 'away_loss' in detail_soup.boxscore.attrs:
					away_loss = detail_soup.boxscore["away_loss"]
				else:
					away_loss = "unknown"
				if 'home_loss' in detail_soup.boxscore.attrs:
					home_loss = detail_soup.boxscore["home_loss"]
				else:
					home_loss = "unknown"
				if detail_soup.find("linescore"):
					away_team_runs = detail_soup.find("linescore")["away_team_runs"]
					home_team_runs = detail_soup.find("linescore")["home_team_runs"]
				else:
					away_team_runs = "unknown"
					home_team_runs = "unknown"
				if away_team_runs > home_team_runs:
					winning_team = "away"
				elif away_team_runs < home_team_runs:
					winning_team = "home"
				else:
					winning_team = "tie"
				if winning_team == "away":
					home_win = 0
				elif winning_team == "home":
					home_win = 1
				for pitch_staff in detail_soup.boxscore.find_all("pitching"):
					if 'team_flag' in pitch_staff.attrs:
						team_flag = pitch_staff["team_flag"]
					else:
						team_flag = "unknown"
					if 'r' in pitch_staff.attrs:
						total_runs = pitch_staff["r"]
					else:
						total_runs = "unknown"
					if 'er' in pitch_staff.attrs:
						total_earned_runs = pitch_staff["er"]
					else:
						total_earned_runs = "unknown"
					for pitcher in pitch_staff.find_all("pitcher"):
						pitcher_id = pitcher["id"]
						if 'name_display_first_last' in pitcher.attrs:
							pitcher_name = pitcher["name_display_first_last"]
						else:
							pitcher_name = pitcher["name"]
							pitcher_name = pitcher_name.replace(',', '')
						p_earned_runs = pitcher["er"]
						p_runs = pitcher["r"]
						p_so = pitcher["so"]
						outs = pitcher["out"]
						p_era = pitcher["era"]
						if 'loss' in pitcher.attrs:
							loss_col = 1
						else:
							loss_col = 0
						if 'win' in pitcher.attrs:
							win_col = 1
						else:
							win_col = 0
						wins = pitcher["w"]
						losses = pitcher["l"]

						pitcher_outfile.write(str(game_id)+","+str(active_date)+","+str(game_pk)+","+str(away_fname)+","+str(home_fname)+","+str(away_id)+","+str(home_id)+","+str(team_flag)+","+str(total_runs)+","+str(total_earned_runs)+","+str(pitcher_id)+","+str(pitcher_name)+","+str(p_runs)+","+str(p_earned_runs)+","+str(outs)+","+str(p_so)+","+str(p_era)+","+str(win_col)+","+str(loss_col)+","+str(wins)+","+str(losses)+"\n")

					n = 0
					for pitcher in pitch_staff.find_all("pitcher"):
						if n == 1:
							break
						else:
							n += 1
						if team_flag == "home":
							home_pitcher = pitcher["id"]
						if team_flag == "away":
							away_pitcher = pitcher["id"]

				for lineup in detail_soup.boxscore.find_all("batting"):
					if 'team_flag' in lineup.attrs:
						team_flag = lineup["team_flag"]
						if team_flag == "home":
							home_lineup = []
						elif team_flag == "away":
							away_lineup = []
						else:
							pass
					else:
						team_flag = "unknown"
					if 'r' in lineup.attrs:
						total_runs = lineup["r"]
					else:
						total_runs = "unknown"
					if 'er' in lineup.attrs:
						total_earned_runs = lineup["er"]
					if 'lob' in lineup.attrs:
						lob = lineup["lob"]
					else:
						total_earned_runs = "unknown"
					for batter in lineup.find_all("batter"):
						batter_id = batter["id"]
						position = batter["pos"]
						if 'name_display_first_last' in batter.attrs:
							batter_name = batter["name_display_first_last"]
						else:
							batter_name = batter["name"]
							batter_name = batter_name.replace(',', '')
						at_bats = batter["ab"]
						hits = batter["h"]
						runs = batter["r"]
						strike_out = batter["so"]
						walk = batter["bb"]
						home_run = batter["hr"]
						double = batter["d"]
						triple = batter["t"]
						rbi = batter["rbi"]
						if "sb" in batter.attrs:
							stolen_bases = batter["sb"]
						else:
							stolen_bases = "unknown"
						if "avg" in batter.attrs:
							avg = batter["avg"]
						else:
							avg = "unknown"
						if "obp" in batter.attrs:
							obp = batter["obp"]
						else:
							obp = "unknown"
						if "slg" in batter.attrs:
							slg = batter["slg"]
						else:
							slg = "unknown"
						if "ops" in batter.attrs:
							slob = batter["ops"]
						else:
							slob = "unknown"

						batter_outfile.write(str(game_id)+","+str(active_date)+","+str(game_pk)+","+str(away_fname)+","+str(home_fname)+","+str(away_id)+","+str(home_id)+","+str(team_flag)+","+str(total_runs)+","+str(total_earned_runs)+","+str(batter_id)+","+str(batter_name)+","+str(position)+","+str(at_bats)+","+str(hits)+","+str(runs)+","+str(strike_out)+","+str(walk)+","+str(home_run)+","+str(double)+","+str(triple)+","+str(rbi)+","+str(stolen_bases)+","+str(avg)+","+str(obp)+","+str(slg)+","+str(slob)+"\n")

					for batter in lineup.find_all("batter"):
						if "bo" in batter.attrs:
							bo = batter["bo"]
							if team_flag == "away" and bo in ["100", "200", "300", "400", "500", "600", "700", "800", "900"]:
								away_lineup.append(batter["id"])
							if team_flag == "home" and bo in ["100", "200", "300", "400", "500", "600", "700", "800", "900"]:
								home_lineup.append(batter["id"])
						else:
							pass

				away_lineup = ':'.join(away_lineup)
				home_lineup = ':'.join(home_lineup)

				boxscore_outfile.write(str(game_id)+","+str(active_date)+","+str(game_pk)+","+str(game_type_des)+","+str(away_fname)+","+str(home_fname)+","+str(away_id)+","+str(home_id)+","+str(home_pitcher)+","+str(away_pitcher)+","+(home_lineup)+","+str(away_lineup)+","+str(away_team_runs)+","+str(home_team_runs)+","+str(home_win)+","+str(winning_team)+","+str(home_wins)+","+str(home_loss)+","+str(away_wins)+","+str(away_loss)+"\n")
		prior_d_url = d_url
