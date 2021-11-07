import os
import pandas as pd
import functions_for_cricbuzz_comm as fcc

og_db_path = os.getcwd()+"\\database\\downloaded_database\\"
comm_all = pd.read_csv(og_db_path+"all_season_details.csv", header=0, delimiter=",")
summ_all = pd.read_csv(og_db_path+"all_season_summary.csv", header=0, delimiter=",")

dic_url_ipl = {2017:"https://www.cricbuzz.com/cricket-series/2568/indian-premier-league-2017/matches", 
				2018:"https://www.cricbuzz.com/cricket-series/2676/indian-premier-league-2018/matches",
				2019:"https://www.cricbuzz.com/cricket-series/2810/indian-premier-league-2019/matches",
				2020:"https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches",
				2021:"https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/matches"}

dic_ipl_team_names = {"PUNJAB KINGS":"PBKS", "KINGS XI PUNJAB":"PBKS",
					"DELHI DAREDEVILS":"DC", "DELHI CAPITALS":"DC",
					"RISING PUNE SUPERGIANT":"RPS", "GUJARAT LIONS":"GL",
					"SUNRISERS HYDERABAD":"SRH", "ROYAL CHALLENGERS BANGALORE":"RCB", 
					"MUMBAI INDIANS":"MI", "KOLKATA KNIGHT RIDERS":"KKR",
					"CHENNAI SUPER KINGS":"CSK", "RAJASTHAN ROYALS":"RR"}

for i in list(dic_url_ipl.keys()):
	url = dic_url_ipl[i]
	links, match_desc = fcc.get_links_for_season_matches(url)
	
	for k in list(dic_ipl_team_names.keys()):
		match_desc = [sub.replace(k,dic_ipl_team_names[k]) for sub in match_desc]
	match_desc = [sub.replace("vs", "v") for sub in match_desc]

	summ_season = summ_all[(summ_all['season'] == i)]

	for k in range(len(links)):
		print("CREATING FOR LINK "+str(k))
		l = k
		if summ_season['short_name'].values[k] == match_desc[l]:
			comm_match = comm_all[(comm_all['match_id'] == summ_season['id'].values[k])]
			comm_buzz = fcc.get_comm(links[k])
			if comm_match['comm_cricbuzz'].size == len(comm_buzz):
				comm_match['comm_cricbuzz'] = comm_buzz
				pd.DataFrame.to_csv(comm_match, os.getcwd()+"\\database\\season_matchwise_database\\"+str(i)+"\\"+str(summ_season['id'].values[k])+".csv", index=False)
			else:
				comm_buzz_df = pd.DataFrame(comm_buzz)
				pd.DataFrame.to_csv(comm_match, os.getcwd()+"\\database\\season_matchwise_database\\"+str(i)+"\\"+str(summ_season['id'].values[k])+"_check.csv", index=False)
				pd.DataFrame.to_csv(comm_buzz_df, os.getcwd()+"\\database\\season_matchwise_database\\"+str(i)+"\\"+str(summ_season['id'].values[k])+"_cricbuzz.csv", index=False)
	break