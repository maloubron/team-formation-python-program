# python program that takes an excel file with consultant + drivers test results as input.
# after running, a simple tkinter interface is run in which the user can enter some input
# gives back an ordered list of all posible consultant teams with most compatible teams on top.


import pandas as pd
from itertools import combinations
import tkinter as tk
from tkinter import *
from tkinter import ttk
from functools import partial
from paretoset import paretoset
import numpy as np
import gpdvega
import altair as alt
import matplotlib.pyplot as plt
import mplcursors
import math 


def combo_lists(df): #this output is only used as input to calculate the friction between consultant pairs
    name_list = []
    for index, row in df.iterrows():
        name_list.append(row[1]) #pak alleen de namen van de excel sheet
    
    consultant_combo2 = list(combinations(name_list, 2)) #all combinations of nr of 2 consultants.
    consultant_combo3 = list(combinations(name_list, 3))
    consultant_combo4 = list(combinations(name_list, 4))

    return consultant_combo2, consultant_combo3, consultant_combo4


def check_skills_MJ(cons_combo, nr_junior, nr_medior, df):
    try:
        value_skill1 = int(skill1_entry.get()) #creates excepts for when the field is left blank
    except ValueError:
        value_skill1 = 0
    try:
        value_skill2 = int(skill2_entry.get())
    except ValueError:
        value_skill2 = 0
    try:
        value_skill3 = int(skill3_entry.get())
    except ValueError:
        value_skill3 = 0
    try:
        value_skill4 = int(skill4_entry.get())
    except ValueError:
        value_skill4 = 0
    try:
        value_skill5 = int(skill5_entry.get())
    except ValueError:
        value_skill5 = 0

    filtered_consultant_teams = []
    for consultant_pair in cons_combo:
        total_junior_pair = 0
        total_medior_pair = 0
        highest_skill1 = 0
        highest_skill2 = 0
        highest_skill3 = 0
        highest_skill4 = 0
        highest_skill5 = 0

        for name in consultant_pair:
            jun_med = df.loc[df['Name'] == name, 'Junior/medior'].iloc[0]
            skill1_level = df.loc[df['Name'] == name, 'Skill1'].iloc[0]
            skill2_level = df.loc[df['Name'] == name, 'Skill2'].iloc[0]
            skill3_level = df.loc[df['Name'] == name, 'Skill3'].iloc[0]
            skill4_level = df.loc[df['Name'] == name, 'Skill4'].iloc[0]
            skill5_level = df.loc[df['Name'] == name, 'Skill5'].iloc[0]
            if jun_med == 'J':
                total_junior_pair += 1
            elif jun_med == 'M':
                total_medior_pair += 1
            else:
                print('Er ging iets fout.')
            #Controleer of elk consultant pair voldoet aan de minimale skill niveau vereisten. In totaal moet er minimaal 1 consultant zijn waarbij de skill level gelijk of hoger is dan de ingevoerde skill level
            if skill1_level >= highest_skill1:
                highest_skill1 = skill1_level
            if skill2_level >= highest_skill2:
                highest_skill2 = skill2_level
            if skill3_level >= highest_skill3:
                highest_skill3 = skill3_level
            if skill4_level >= highest_skill4:
                highest_skill4 = skill4_level
            if skill5_level >= highest_skill5:
                highest_skill5 = skill5_level

        if highest_skill1 >= value_skill1 and highest_skill2 >= value_skill2 and highest_skill3 >= value_skill3 and highest_skill4 >= value_skill4 and highest_skill5 >= value_skill5:
            skills_met = True
        else:
            skills_met = False
        if total_junior_pair >= nr_junior and total_medior_pair >= nr_medior and skills_met:
            filtered_consultant_teams.append(consultant_pair)
    return filtered_consultant_teams


def friction(consultant_combo2, df):
    friction_dict = {}
    for consultant_pair in consultant_combo2:
        friction = 0 #herstart at each consultant pair
        #for name in consultant_pair:
        cons1 = consultant_pair[0]
        cons2 = consultant_pair[1]
        #expressions
        yellow_ex1 = df.loc[df['Name'] == cons1, 'Yellow'].iloc[0]
        yellow_ex2 = df.loc[df['Name'] == cons2, 'Yellow'].iloc[0]
        green_ex1 = df.loc[df['Name'] == cons1, 'Green'].iloc[0]
        green_ex2 = df.loc[df['Name'] == cons2, 'Green'].iloc[0]
        red_ex1 = df.loc[df['Name'] == cons1, 'Red'].iloc[0]
        red_ex2 = df.loc[df['Name'] == cons2, 'Red'].iloc[0]
        blue_ex1 = df.loc[df['Name'] == cons1, 'Blue'].iloc[0]
        blue_ex2 = df.loc[df['Name'] == cons2, 'Blue'].iloc[0]
        orange_ex1 = df.loc[df['Name'] == cons1, 'Orange'].iloc[0]
        orange_ex2 = df.loc[df['Name'] == cons2, 'Orange'].iloc[0]
        purple_ex1 = df.loc[df['Name'] == cons1, 'Purple'].iloc[0]
        purple_ex2 = df.loc[df['Name'] == cons2, 'Purple'].iloc[0]
        turquoise_ex1 = df.loc[df['Name'] == cons1, 'Turquoise'].iloc[0]
        turquoise_ex2 = df.loc[df['Name'] == cons2, 'Turquoise'].iloc[0]

        #resistance
        yellow_res1 = df.loc[df['Name'] == cons1, 'YellowR'].iloc[0]
        yellow_res2 = df.loc[df['Name'] == cons2, 'YellowR'].iloc[0]
        green_res1 = df.loc[df['Name'] == cons1, 'GreenR'].iloc[0]
        green_res2 = df.loc[df['Name'] == cons2, 'GreenR'].iloc[0]
        red_res1 = df.loc[df['Name'] == cons1, 'RedR'].iloc[0]
        red_res2 = df.loc[df['Name'] == cons2, 'RedR'].iloc[0]
        blue_res1 = df.loc[df['Name'] == cons1, 'BlueR'].iloc[0]
        blue_res2 = df.loc[df['Name'] == cons2, 'BlueR'].iloc[0]
        orange_res1 = df.loc[df['Name'] == cons1, 'OrangeR'].iloc[0]
        orange_res2 = df.loc[df['Name'] == cons2, 'OrangeR'].iloc[0]
        purple_res1 = df.loc[df['Name'] == cons1, 'PurpleR'].iloc[0]
        purple_res2 = df.loc[df['Name'] == cons2, 'PurpleR'].iloc[0]
        turquoise_res1 = df.loc[df['Name'] == cons1, 'TurquoiseR'].iloc[0]
        turquoise_res2 = df.loc[df['Name'] == cons2, 'TurquoiseR'].iloc[0]
        #print(consultant_pair, cons1, cons2)
        #check for each color if one consultant has an expression above 15 for one color, while at the same time the other consultant has a resitance above 15 for that color.
        #note that one person can have both an expression and resistance on same color. Whether someone gets a resitance on a certain color depends from person to person.
        #Yellow
        if yellow_ex1 >= 15 and yellow_res2 <= -15: #normal friction
            if yellow_ex1 >=30 and yellow_res2 <= -20: #extra friction
                friction+= 1.5
            else:
                friction+=1
        if yellow_ex2 >= 15 and yellow_res1 <= -15:
            if yellow_ex2 >= 30 and yellow_res1 <= -20:
                friction+=1.5
            else:
                friction+=1
        if yellow_ex1 >= 25 and yellow_ex2 >= 25: #we want friciton to be smaller for people who both score really high on same color
            friction-=1
        #Green
        if green_ex1 >= 15 and green_res2 <= -15:
            if green_ex1>=30 and green_res2<=-20:
                friction+=1.5
            else:
                friction+=1
        if green_ex2 >= 15 and green_res1 <= -15:
            if green_ex2 >=30 and green_res1 <=-20:
                friction+=1.5
            else:
                friction+=1
        if green_ex1 >= 25 and green_ex2 >= 25: #we want friciton to be smaller for people who both score really high on same color
            friction-=1
        #Red
        if red_ex1 >= 15 and red_res2 <= -15:
            if red_ex1 >= 30 and red_res2 <= -20:
                friction+=1.5
            else:
                friction+=1
        if red_ex2 >= 15 and red_res1 <= -15:
            if red_ex2>=30 and red_res1 <= -20:
                friction+=1.5
            else:
                friction+=1
        if red_ex1 >= 25 and red_ex2 >= 25: #we want friciton to be smaller for people who both score really high on same color
            friction-=1
        #Blue
        if blue_ex1 >= 15 and blue_res2 <= -15:
            if blue_ex1 >= 30 and blue_res2 <= -20:
                friction += 1.5
            else:
                friction+=1
        if blue_ex2 >= 15 and blue_res1 <= -15:
            if blue_ex2 >= 30 and blue_res1 <= -20:
                friction+=1.5
            else:
                friction+=1
        if blue_ex1 >= 25 and blue_ex2 >= 25: #we want friciton to be smaller for people who both score really high on same color
            friction-=1
        #Orange
        if orange_ex1 >= 15 and orange_res2 <= -15:
            if orange_ex1 >= 30 and orange_res2 <= -20:
                friction+=1.5
            else:
                friction+=1
        if orange_ex2 >= 15 and orange_res1 <= -15:
            if orange_ex2 >= 30 and orange_res1 <= -20:
                friction+=1.5
            else:
                friction+=1
        if orange_ex1 >= 25 and orange_ex2 >= 25: #we want friciton to be smaller for people who both score really high on same color
            friction-=1
        #Purple
        if purple_ex1 >= 15 and purple_res2 <= -15:
            if purple_ex1 >= 30 and purple_res2 <= -20:
                friction += 1.5
            else:
                friction+=1
        if purple_ex2 >= 15 and purple_res1 <= -15:
            if purple_ex2 >= 30 and purple_res1 <= -20:
                friction+=1.5
            else:
                friction+=1
        if purple_ex1 >= 25 and purple_ex2 >= 25: #we want friciton to be smaller for people who both score really high on same color
            friction-=1
        #Turquoise
        if turquoise_ex1 >= 15 and turquoise_res2 <= -15:
            if turquoise_ex1 >= 30 and turquoise_res2 <= -20:
                friction +=1.5
            else:
                friction+=1
        if turquoise_ex2 >= 15 and turquoise_res1 <= -15:
            if turquoise_ex2 >= 30 and turquoise_res1 <= -20:
                friction+=1.5
            else:
                friction+=1
        if turquoise_ex1 >= 25 and turquoise_ex2 >= 25: #we want friciton to be smaller for people who both score really high on same color
            friction-=1

        if friction <= 0:
            final_fric = 0 #this happens in the rare case when 2 people have no firction and on some color both 25 or higher. we want 0 to be the lowest friction nr
        else:
            final_fric = friction

        friction_dict[consultant_pair] = final_fric
    return friction_dict


def color_cov(filtered_teams, df):
    results = []
    for team in filtered_teams:
        coverage = []
        for member in team:
            yellow = df.loc[df['Name'] == member, 'Yellow'].iloc[0]
            if yellow >= 15:
                coverage.append('yellow')
            green = df.loc[df['Name'] == member, 'Green'].iloc[0]
            if green >= 15:
                coverage.append('green')
            blue = df.loc[df['Name'] == member, 'Blue'].iloc[0]
            if blue >= 15:
                coverage.append('blue')
            red = df.loc[df['Name'] == member, 'Red'].iloc[0]
            if red >= 15:
                coverage.append('red')
            purple = df.loc[df['Name'] == member, 'Purple'].iloc[0]
            if purple >= 15:
                coverage.append('purple')
            orange = df.loc[df['Name'] == member, 'Orange'].iloc[0]
            if orange >= 15:
                coverage.append('orange')
            turquoise = df.loc[df['Name'] == member, 'Turquoise'].iloc[0]
            if turquoise >= 15:
                coverage.append('turquoise')
        quality_coverage = len(coverage) #sometimes multiple people have the same color. Coverage can have max of 7, with quality you can distinguish difference between coverage with the same value
        #final_coverage_team = set(coverage)
        final_coverage_team = coverage

        result = (team, 'total number of summed colors:', quality_coverage, 'color coverage (max7):', final_coverage_team)
        results.append(result)

    return results

def team_friction(dic, teams):
    results = []
    for team in teams:
        total_fric = 0
        pairs_of2 = []
        if len(team) == 2:
            total_fric = dic[team]

        else:
            pairs_of2 = list(combinations(team, 2))
            for pair in pairs_of2:
                pair_fric = dic[pair]
                total_fric = total_fric + pair_fric
        results.append((team, 'total friction:', total_fric))
    return results

def count_colors(color_list): #first unique color gets one point, if the same color occurs multiple times, it gets divided by 2 each time. So second color gets 0.5 added, third one 0.25 and so forth. 
    color_counts = {}
    for color in color_list:
        if color in color_counts:
            color_counts[color] += 1
        else:
            color_counts[color] = 1

    total_count = 0
    for count in color_counts.values():
        divisor = 1
        for _ in range(count):
            total_count += 1 / divisor
            divisor *= 2

    return total_count


def calculate_sample_std_dev(list_of_numbers):
    n = len(list_of_numbers)
    try:
        mean = sum(list_of_numbers) / n
    except ZeroDivisionError:
        n = 0.1
        mean = sum(list_of_numbers) / n
    variance = sum((x - mean) ** 2 for x in list_of_numbers) / (n - 1)
    sample_std_dev = math.sqrt(variance)
    return sample_std_dev

def ordered_results(fric, coverage):
    list_results =[]
    final_results = []
    for i in range(len(fric)):
        new_fric = fric[i][-2:]
        list_results.append((coverage[i], new_fric))

    #print(list_results)
    total_nr_results = len(list_results)
    total_friction_all_teams = 0
    total_color_cov_all_teams = 0
    list_all_color_coverages = []
    list_all_frictions = []
    for result in list_results:
        nr_colors = count_colors(result[0][4])
        total_color_cov_all_teams+=nr_colors
        list_all_color_coverages.append(nr_colors)
        friction_total = result[1][1]
        total_friction_all_teams +=friction_total
        list_all_frictions.append(friction_total)

    try:
        mean_color_cov = total_color_cov_all_teams/total_nr_results #divide the nr of results (teams) by the summed up color coverage to get mean
    except ZeroDivisionError:
        #print(total_color_cov_all_teams, total_nr_results, result)
        mean_color_cov = 0.1

    try:
        mean_friction = total_friction_all_teams/total_nr_results
    except ZeroDivisionError:
        #print(total_friction_all_teams, total_nr_results, result)
        mean_friction = 0.1
    std_dev_color_cov1 = calculate_sample_std_dev(list_all_color_coverages)
    std_dev_friction1 = calculate_sample_std_dev(list_all_frictions)

    if std_dev_color_cov1 == 0: #I cant divide by 0
        std_dev_color_cov = 0.1
    else:
        std_dev_color_cov = std_dev_color_cov1
    if std_dev_friction1 == 0:
        std_dev_friction = 0.1
    else:
        std_dev_friction = std_dev_friction1

    #T-score = (X - μ) / (s / sqrt(n)) --> you need mean and standard dev
    #X is the value you want to calculate the T-score for
    #μ is the sample mean of the list
    #s is the sample standard deviation of the list
    #n is the sample size (i.e., the number of values in the list)

    for result in list_results:
        team_results = []
        color_coverage2 = count_colors(result[0][4])
        friction2 = result[1][1]

        t_score_color_cov = (color_coverage2 - mean_color_cov) / (std_dev_color_cov / math.sqrt(len(list_results)))
        t_score_friction = (friction2 - mean_friction) / (std_dev_friction / math.sqrt(len(list_results)))
        print(result, color_coverage2, friction2)

        #print('fric t score:', t_score_friction, result[0][0])
        minus = t_score_color_cov - t_score_friction
        team_results.append(result[0][0]) #names of team members
        team_results.append(round(t_score_color_cov, 3))
        team_results.append(round(t_score_friction, 3))
        team_results.append(round(minus,3))
        final_results.append(team_results)

    #print(final_results)
    sorted_final_results = sorted(final_results, key=lambda x: x[3], reverse=True)
    return sorted_final_results


def check_team_size(): #kijkt hoe groot het team moet zijn en geeft op basis daarvan de juiste paraeters mee 
    data_excel = pd.read_excel('Testdata.xlsx') #the input file, check that columns and layout is exactly the same as Testdata.xlsx

    excluded_cons = ex_con_entry.get().split(',')

    new_df = pd.DataFrame(columns=data_excel.columns)

    for index, row in data_excel.iterrows():
        if row['Name'] in excluded_cons: 
            print(f"{row['Name']} found in input, skipping...")
        else:
            new_df = pd.concat([new_df, row.to_frame().transpose()], ignore_index=True)

    combi1 = combo_lists(new_df)[0] 
    combi2 = combo_lists(new_df)[1]
    combi3 = combo_lists(new_df)[2]

    value_team_size = float(team_size_entry.get())

    try:
        value_nr_junior = float(nr_junior_entry.get())
    except:
        value_nr_junior = 0.0
    try:
        value_nr_medior = float(nr_medior_entry.get())
    except:
        value_nr_medior = 0.0
    friction_dictionary = friction(combi1, new_df)

    if value_team_size ==2:
        filtered_teams = check_skills_MJ(combi1, value_nr_junior, value_nr_medior, new_df)
        color_coverage = color_cov(filtered_teams, new_df)
        team_fric = team_friction(friction_dictionary, filtered_teams)
        #print(team_fric, color_coverage)
        result = (team_fric, color_coverage)

       
    elif value_team_size ==3:
        filtered_teams3 = check_skills_MJ(combi2, value_nr_junior, value_nr_medior, new_df)
        color_coverage = color_cov(filtered_teams3, new_df)
        team_fric = team_friction(friction_dictionary, filtered_teams3)
        #print(team_fric, color_coverage)
        result = (team_fric, color_coverage)

    elif value_team_size ==4:
        filtered_teams4 = check_skills_MJ(combi3, value_nr_junior, value_nr_medior, new_df)
        color_coverage = color_cov(filtered_teams4, new_df)
        team_fric = team_friction(friction_dictionary, filtered_teams4)
        #print(team_fric, color_coverage)
        result = (team_fric, color_coverage)

    else:
        filtered_teams = []
    #return filtered_teams


    ordered_res = ordered_results(team_fric, color_coverage)
    #print(ordered_res)


    show_results(ordered_res)


def show_results(filtered_teams): #maakt een tabel van de resultaten
    # verwijder de oude tabel (als die er is)
    for widget in window.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()

    # maak een nieuwe tabel
    cols = ('Team members', 'T-score color coverage, higher is better', 'T-score friction, lower is better', 'Score')
    tree = ttk.Treeview(window, columns=cols, show='headings')

    # zet de kolomnamen
    for col in cols:
        tree.heading(col, text=col)

    # voeg de data toe aan de tabel
    for team in filtered_teams:
        if len(team) == 2:
            tree.insert("", tk.END, values=(team[0], team[1]))
        elif len(team) == 3:
            tree.insert("", tk.END, values=(team[0], team[1], team[2]))
        elif len(team) == 4:
            tree.insert("", tk.END, values=(team[0], team[1], team[2], team[3]))

    # toon de tabel in het venster
    tree.pack()




#makes a simple interface in Tkinter in which user can give some input
window = tk.Tk()

# maak de frames aan voor elke invoer
team_size_frame = tk.Frame(window)
nr_junior_frame = tk.Frame(window)
nr_medior_frame = tk.Frame(window)
skill1_frame = tk.Frame(window)
skill2_frame = tk.Frame(window)
skill3_frame = tk.Frame(window)
skill4_frame = tk.Frame(window)
skill5_frame = tk.Frame(window)
excluded_cons_frame = tk.Frame(window)

# voeg de labels toe aan de frames
tk.Label(team_size_frame, text="Hoeveel mensen wil je in je team?").grid(row=0, column=0)
tk.Label(nr_junior_frame, text="Hoeveel junior consultants wil je minimaal in je team?").grid(row=1, column=0)
tk.Label(nr_medior_frame, text="Hoeveel medior consultants wil je minimaal in je team?").grid(row=2, column=0)
tk.Label(skill1_frame, text="Welk level van skill 1 moet het team minimaal bevatten?").grid(row=3, column=0)
tk.Label(skill2_frame, text="Welk level van skill 2 moet het team minimaal bevatten?").grid(row=4, column=0)
tk.Label(skill3_frame, text="Welk level van skill 3 moet het team minimaal bevatten?").grid(row=5, column=0)
tk.Label(skill4_frame, text="Welk level van skill 4 moet het team minimaal bevatten?").grid(row=6, column=0)
tk.Label(skill5_frame, text="Welk level van skill 5 moet het team minimaal bevatten?").grid(row=7, column=0)
tk.Label(excluded_cons_frame, text="Welke consultants moeten we niet meenemen?").grid(row=8, column=0)

# voeg de input widgets toe aan de frames
team_size_entry = tk.Entry(team_size_frame)
team_size_entry.grid(row=0, column=1)
nr_junior_entry = tk.Entry(nr_junior_frame)
nr_junior_entry.grid(row=1, column=1)
nr_medior_entry = tk.Entry(nr_medior_frame)
nr_medior_entry.grid(row=2, column=1)
skill1_entry = tk.Entry(skill1_frame)
skill1_entry.grid(row=3, column=1)
skill2_entry = tk.Entry(skill2_frame)
skill2_entry.grid(row=4, column=1)
skill3_entry = tk.Entry(skill3_frame)
skill3_entry.grid(row=5, column=1)
skill4_entry = tk.Entry(skill4_frame)
skill4_entry.grid(row=6, column=1)
skill5_entry = tk.Entry(skill5_frame)
skill5_entry.grid(row=7, column=1)
ex_con_entry = tk.Entry(excluded_cons_frame)
ex_con_entry.grid(row=8, column=1)
#weight_friction_entry = tk.Entry(weight_friction_frame)
#weight_friction_entry.grid(row=8, column=1)
#weight_coverage_entry = tk.Entry(weight_coverage_frame)
#weight_coverage_entry.grid(row=9, column=1)

# plaats de frames met de widgets in de window
team_size_frame.pack()
nr_junior_frame.pack()
nr_medior_frame.pack()
skill1_frame.pack()
skill2_frame.pack()
skill3_frame.pack()
skill4_frame.pack()
skill5_frame.pack()
excluded_cons_frame.pack()
#weight_friction_frame.pack()
#weight_coverage_frame.pack()


# voeg een knop toe
button = tk.Button(window, text="Bereken", command=partial(check_team_size))
button.pack()
result_label = tk.Label(window, text="Resultaat: ")
result_label.pack()
window.mainloop()

#if __name__ == '__main__':
 #   main()

