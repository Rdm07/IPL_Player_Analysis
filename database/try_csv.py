import os
import pandas as pd
import functions_for_cricbuzz_comm as fcc

og_db_path = os.getcwd()+"\\database\\downloaded_database\\"
comm_match = pd.read_csv(og_db_path+"2017_1st_match.csv", header=0, delimiter=",")

comm_cric = fcc.get_comm("https://www.cricbuzz.com/cricket-full-commentary/18121/srh-vs-rcb-1st-match-indian-premier-league-2017")
comm_cric_df = pd.DataFrame(comm_cric)
# comm_match['comm_cricbuzz'] = comm_cric

pd.DataFrame.to_csv(comm_cric_df, os.getcwd()+"\\database\\season_matchwise_database\\2017\\match_01.csv")