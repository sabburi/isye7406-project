import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from collections import defaultdict

def agg_features(main_df):
    goals_for_dict = defaultdict(lambda : defaultdict(int))
    goals_against_dict = defaultdict(lambda : defaultdict(int))
    home_goals_for = []
    away_goals_for = []
    home_goals_against = []
    away_goals_against = []

    shots_dict = defaultdict(lambda : defaultdict(int))
    shots_tgt_dict = defaultdict(lambda : defaultdict(int))
    home_shots = []
    home_shots_tgt = []
    away_shots = []
    away_shots_tgt = []

    shots_against_dict = defaultdict(lambda : defaultdict(int))
    shots_tgt_against_dict = defaultdict(lambda : defaultdict(int))
    home_shots_against = []
    home_shots_tgt_against = []
    away_shots_against = []
    away_shots_tgt_against = []

    fk_concede_dict = defaultdict(lambda : defaultdict(int))
    home_fk_concede = []
    away_fk_concede = []

    fk_won_dict = defaultdict(lambda : defaultdict(int))
    home_fk_won = []
    away_fk_won = []

    new_chem_dict = defaultdict(float)
    home_new_chem = []
    away_new_chem = []

    win_dict = defaultdict(lambda : defaultdict(int))
    home_wins = []
    away_wins = []

    loss_dict = defaultdict(lambda : defaultdict(int))
    home_losses = []
    away_losses = []

    draw_dict = defaultdict(lambda : defaultdict(int))
    home_draws = []
    away_draws = []

    for i, row in main_df.iterrows():

        goals_for_dict[row['Season']][row['HomeTeam']] += row['FTHG']
        home_goals_for.append(goals_for_dict[row['Season']][row['HomeTeam']])

        goals_for_dict[row['Season']][row['AwayTeam']] += row['FTAG']
        away_goals_for.append(goals_for_dict[row['Season']][row['AwayTeam']])

        goals_against_dict[row['Season']][row['HomeTeam']] += row['FTAG']
        home_goals_against.append(goals_against_dict[row['Season']][row['HomeTeam']])

        goals_against_dict[row['Season']][row['AwayTeam']] += row['FTHG']
        away_goals_against.append(goals_against_dict[row['Season']][row['AwayTeam']])

        shots_dict[row['Season']][row['HomeTeam']] += row['HS']
        home_shots.append(shots_dict[row['Season']][row['HomeTeam']])
        shots_dict[row['Season']][row['AwayTeam']] += row['AS']
        away_shots.append(shots_dict[row['Season']][row['AwayTeam']])

        shots_tgt_dict[row['Season']][row['HomeTeam']] += row['HST']
        home_shots_tgt.append(shots_tgt_dict[row['Season']][row['HomeTeam']])
        shots_tgt_dict[row['Season']][row['AwayTeam']] += row['AST']
        away_shots_tgt.append(shots_tgt_dict[row['Season']][row['AwayTeam']])

        shots_against_dict[row['Season']][row['HomeTeam']] += row['AS']
        home_shots_against.append(shots_against_dict[row['Season']][row['HomeTeam']])
        shots_against_dict[row['Season']][row['AwayTeam']] += row['HS']
        away_shots_against.append(shots_against_dict[row['Season']][row['AwayTeam']])

        shots_tgt_against_dict[row['Season']][row['HomeTeam']] += row['AST']
        home_shots_tgt_against.append(shots_tgt_against_dict[row['Season']][row['HomeTeam']])
        shots_tgt_against_dict[row['Season']][row['AwayTeam']] += row['HST']
        away_shots_tgt_against.append(shots_tgt_against_dict[row['Season']][row['AwayTeam']])

        fk_concede_dict[row['Season']][row['HomeTeam']] += row['HF']
        home_fk_concede.append(fk_concede_dict[row['Season']][row['HomeTeam']])
        fk_concede_dict[row['Season']][row['AwayTeam']] += row['AF']
        away_fk_concede.append(fk_concede_dict[row['Season']][row['AwayTeam']])

        fk_won_dict[row['Season']][row['HomeTeam']] += row['AF']
        home_fk_won.append(fk_won_dict[row['Season']][row['HomeTeam']])
        fk_won_dict[row['Season']][row['AwayTeam']] += row['HF']
        away_fk_won.append(fk_won_dict[row['Season']][row['AwayTeam']])

        if row['HomeTeam'] not in new_chem_dict.keys():
            new_chem_dict[row['HomeTeam']] = row['ChemHome']

        if row['AwayTeam'] not in new_chem_dict.keys():
            new_chem_dict[row['AwayTeam']] = row['ChemAway']
            
        

        if row['FTR'] == 'H':
            new_chem_dict[row['HomeTeam']] += row['ChemDeltaHome']
            home_new_chem.append(new_chem_dict[row['HomeTeam']])

            new_chem_dict[row['AwayTeam']] -= row['ChemDeltaAway']
            away_new_chem.append(new_chem_dict[row['AwayTeam']])

            win_dict[row['Season']][row['HomeTeam']] += 1
            home_wins.append(win_dict[row['Season']][row['HomeTeam']])
            away_wins.append(win_dict[row['Season']][row['AwayTeam']])

            loss_dict[row['Season']][row['AwayTeam']] += 1
            home_losses.append(loss_dict[row['Season']][row['HomeTeam']])
            away_losses.append(loss_dict[row['Season']][row['AwayTeam']])

            home_draws.append(draw_dict[row['Season']][row['HomeTeam']])
            away_draws.append(draw_dict[row['Season']][row['AwayTeam']])              

        elif row['FTR'] == 'A':

            new_chem_dict[row['AwayTeam']] += row['ChemDeltaAway']
            away_new_chem.append(new_chem_dict[row['AwayTeam']])

            new_chem_dict[row['HomeTeam']] -= row['ChemDeltaHome']
            home_new_chem.append(new_chem_dict[row['HomeTeam']])

            win_dict[row['Season']][row['AwayTeam']] += 1
            home_wins.append(win_dict[row['Season']][row['HomeTeam']])
            away_wins.append(win_dict[row['Season']][row['AwayTeam']])

            loss_dict[row['Season']][row['HomeTeam']] += 1
            home_losses.append(loss_dict[row['Season']][row['HomeTeam']])
            away_losses.append(loss_dict[row['Season']][row['AwayTeam']])

            home_draws.append(draw_dict[row['Season']][row['HomeTeam']])
            away_draws.append(draw_dict[row['Season']][row['AwayTeam']])  
        
        else:
            new_chem_dict[row['HomeTeam']] += row['ChemDeltaHome'] / 2
            home_new_chem.append(new_chem_dict[row['HomeTeam']])

            new_chem_dict[row['AwayTeam']] += row['ChemDeltaAway'] / 2
            away_new_chem.append(new_chem_dict[row['AwayTeam']])   

            home_wins.append(win_dict[row['Season']][row['HomeTeam']])
            away_wins.append(win_dict[row['Season']][row['AwayTeam']])

            home_losses.append(loss_dict[row['Season']][row['HomeTeam']])
            away_losses.append(loss_dict[row['Season']][row['AwayTeam']])

            draw_dict[row['Season']][row['HomeTeam']] += 1
            draw_dict[row['Season']][row['AwayTeam']] += 1
            home_draws.append(draw_dict[row['Season']][row['HomeTeam']])
            away_draws.append(draw_dict[row['Season']][row['AwayTeam']])           

    main_df['HomeGoalsFor'] = home_goals_for
    main_df['AwayGoalsFor'] = away_goals_for
    main_df['HomeGoalsAgainst'] = home_goals_against
    main_df['AwayGoalsAgainst'] = away_goals_against
    main_df['HomeShots'] = home_shots
    main_df['AwayShots'] = away_shots
    main_df['HomeShotsAgainst'] = home_shots_against
    main_df['AwayShotsAgainst'] = away_shots_against
    main_df['HomeShotsTgt'] = home_shots_tgt
    main_df['AwayShotsTgt'] = away_shots_tgt
    main_df['HomeShotsTgtAgainst'] = home_shots_tgt_against
    main_df['AwayShotsTgtAgainst'] = away_shots_tgt_against
    main_df['HomeFKC'] = home_fk_concede
    main_df['AwayFKC'] = away_fk_concede
    main_df['HomeFKW'] = home_fk_won
    main_df['AwayFKW'] = away_fk_won
    main_df['HomeNewChem'] = home_new_chem
    main_df['AwayNewChem'] = away_new_chem
    main_df['HomeWins'] = home_wins
    main_df['AwayWins'] = away_wins
    main_df['HomeLosses'] = home_losses
    main_df['AwayLosses'] = away_losses
    main_df['HomeDraws'] = home_draws
    main_df['AwayDraws'] = away_draws

    return main_df

def differences(main_df):
    home_cols = [col for col in main_df.columns if (col.startswith('Home') or col.endswith('Home')) and is_numeric_dtype(main_df[col])]
    away_cols = [col for col in main_df.columns if (col.startswith('Away') or col.endswith('Away')) and is_numeric_dtype(main_df[col])]
    x = defaultdict(list)
    for i, row in main_df.iterrows():
        for h, a in zip(home_cols, away_cols):
            x[h.replace('Home', 'Diff')].append(row[h] - row[a])
    for key in x:
        main_df[key] = x[key]

    return main_df

def calc_upset(x, thresh_h, thresh_a, thresh_d1, thresh_d2):
    if x['FTR'] == 'H' and 1 / float(x['B365H']) < thresh_h:
        return 1
    elif x['FTR'] == 'A' and 1 / float(x['B365A']) < thresh_a:
        return 1
    elif x['FTR'] == 'D' and 1 / float(x['B365D']) < thresh_d1:
        return 1
    elif (x['FTR'] == 'H' or x['FTR'] == 'A') and 1 / float(x['B365D']) > thresh_d2:
        return 1
    else:
        return 0


def upset(main_df, h_thresh, a_thresh, d_1_thresh, d_2_thresh):
    upset = [calc_upset(row, h_thresh, a_thresh, d_1_thresh, d_2_thresh) for i, row in main_df.iterrows()]

    main_df['Upset'] = np.array(upset).reshape(-1, 1)

    return main_df



