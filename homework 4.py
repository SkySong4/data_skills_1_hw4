# PPHA 30537
# Spring 2023
# Homework 4

# Tianhua Song
# SkySong4

# Due date: Sunday April 23rd before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.  Using functions for organization will be rewarded.

##################

# To answer these questions, you will use the csv document included in
# your repo.  In nst-est2022-alldata.csv: SUMLEV is the level of aggregation,
# where 10 is the whole US, and other values represent smaller geographies. 
# REGION is the fips code for the US region. STATE is the fips code for the 
# US state.  The other values are as per the data dictionary at:
# https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2022/NST-EST2022-ALLDATA.pdf
# Note that each question will build on the modified dataframe from the
# question before.  Make sure the SettingWithCopyWarning is not raised.

import copy
import os
import pandas as pd
import us

# Question 1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.
BASE_DIR = r"D:\\data_skills_1_hw4"


def load_df(csv_filename):
    abs_path = os.path.join(BASE_DIR, csv_filename)
    return pd.read_csv(abs_path)


# Question 2: Your data only includes fips codes for states.  Use the us
# library to crosswalk fips codes to state abbreviations.  Keep only the
# state abbreviations in your data.
def q2(df):
    df = df[df["STATE"] != 0]
    df = df[df["STATE"] != 72]
    def fips_to_abbr(fips_code):
        state = us.states.lookup(str(fips_code).zfill(2))
        return state.abbr if state else None
    df["State_Abbreviation"] = df["STATE"].apply(fips_to_abbr)
    return df


# Question 3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize it for them.  Show 
# some relevant exploration output with print() statements.
    # Answer for q3(print at the end)
    #print("\nAnswer for q3:")
    #print(df.shape)
    #print(df.head(10))
    #print(df.tail(10))
    #print(df.describe())



# Question 4: Subset the data so that only observations for individual
# US states remain, and only state abbreviations and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.
def q4(df):
    return df[["State_Abbreviation", "POPESTIMATE2020", "POPESTIMATE2021", "POPESTIMATE2022"]]


# Question 5: Show only the 10 largest states by 2021 population estimates, in
# decending order.
def q5(df):
    return df.sort_values("POPESTIMATE2021", ascending=False).head(10)


# Question 6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?
def q6(df):
    df_6 = copy.deepcopy(df)
    df_6.loc[:, "POPCHANGE"] = df_6["POPESTIMATE2022"] - df_6["POPESTIMATE2020"]
    gained_population = len(df_6[df_6["POPCHANGE"] > 0])
    lost_population = len(df_6[df_6["POPCHANGE"] < 0])
    return df_6, gained_population, lost_population


# Question 7: Show all the states that had an estimated change of smaller 
# than 1000 people. (hint: look at the standard abs function)
def a7(df):
     return df[df["POPCHANGE"].abs() < 1000]


# Question 8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.
def a8(df):
    popchange_std = df["POPCHANGE"].std()
    largepopchange_states = df[df["POPCHANGE"].abs() > popchange_std]
    # sort by absolute number
    # largepopchange_states = largepopchange_states.sort_values("POPCHANGE", key=lambda x: x.abs(), ascending=False)
    # sort by real number
    largepopchange_states = largepopchange_states.sort_values(by="POPCHANGE", ascending=False)
    return largepopchange_states


if __name__ == '__main__':
    csv_filename = "NST-EST2022-ALLDATA.csv"
    df = load_df(csv_filename)

    # Answer for q2
    df = q2(df)
    df_2 = df[['State_Abbreviation']]
    print("\nAnswer for q2:")
    print(df_2)
    
    # Answer for q3
    print("\nAnswer for q3:")
    print(df.shape)
    print(df.head())
    print(df.tail())
    print(df.describe())
    
    # Answer for q4
    df_4 = q4(df)
    print("\nAnswer for q4:")
    print(df_4)

    # Answer for q5
    df_5 = q5(df_4)
    print("\nAnswer for q5:")
    print(df_5)

    # Answer for q6
    print("\nAnswer for q6:")
    df_6, gained_population, lost_population = q6(df_4)
    print(f"Number of states that gained population: {gained_population}")
    print(f"Number of states that lost population: {lost_population}")

    # Answer for q7
    df_7 = a7(df_6)
    print("\nAnswer for q7:")
    print(df_7['State_Abbreviation'])

    # Answer for q8
    df_8 = a8(df_6)
    print("\nAnswer for q8:")
    print(df_8[['State_Abbreviation', 'POPCHANGE']])
