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

# Question 1: Load the population estimates file into a dataframe. Specify
# an absolute path using the Python os library to join filenames, so that
# anyone who clones your homework repo only needs to update one for all
# loading to work.

import pandas as pd
import os

# specify the absolute path to the csv file
base_path = 'C:\Users\ROG\Documents\GitHub\homework-4'
filename = 'NST-EST2022-ALLDATA.csv'
abs_path = os.path.join(base_path, filename)

# load the csv file into a pandas dataframe
population_estimates = pd.read_csv(abs_path)

print(population_estimates.head())

# Question 2: Your data only includes fips codes for states.  Use the us
# library to crosswalk fips codes to state abbreviations.  Keep only the
# state abbreviations in your data.


import us

# Function to convert FIPS code to state abbreviation
def fips_to_abbr(fips_code):
    state = us.states.lookup(str(fips_code).zfill(2))
    return state.abbr if state else None

# Apply the function to the STATE column and store the result in a new column
population_estimates["State_Abbreviation"] = population_estimates["STATE"].apply(fips_to_abbr)

# Drop the original STATE column
population_estimates.drop("STATE", axis=1, inplace=True)

print(population_estimates.head())

# Question 3: Then show code doing some basic exploration of the
# dataframe; imagine you are an intern and are handed a dataset that your
# boss isn't familiar with, and asks you to summarize it for them.  Show 
# some relevant exploration output with print() statements.

# Exploration and summary
print("Shape of the DataFrame:")
print(population_estimates.shape)
print("\nData types of the columns:")
print(population_estimates.dtypes)
print("\nFirst few rows:")
print(population_estimates.head())
print("\nSummary statistics:")
print(population_estimates.describe())
print("\nMissing values:")
print(population_estimates.isnull().sum())
print("\nUnique values in SUMLEV:")
print(population_estimates["SUMLEV"].unique())
print("\nUnique values in REGION:")
print(population_estimates["REGION"].unique())


# Question 4: Subset the data so that only observations for individual
# US states remain, and only state abbreviations and data for the population
# estimates in 2020-2022 remain.  The dataframe should now have 4 columns.

# Select only include individual US states
state_data = population_estimates[population_estimates["SUMLEV"] != 10]

# Select only state abbreviations and population estimates for 2020-2022
state_data = state_data[["State_Abbreviation", "POPESTIMATE2020", "POPESTIMATE2021", "POPESTIMATE2022"]]

print(state_data.head())

# Question 5: Show only the 10 largest states by 2021 population estimates, in
# decending order.

state_data = state_data.sort_values("POPESTIMATE2021", ascending=False)

print(state_data.head(10))

# Question 6: Create a new column, POPCHANGE, that is equal to the change in
# population from 2020 to 2022.  How many states gained and how many lost
# population between these estimates?

# Calculate the population change from 2020 to 2022 and store it in a new column
state_data["POPCHANGE"] = state_data["POPESTIMATE2022"] - state_data["POPESTIMATE2020"]

# Count the number of states with positive and negative population change
gained_population = len(state_data[state_data["POPCHANGE"] > 0])
lost_population = len(state_data[state_data["POPCHANGE"] < 0])

print(f"Number of states that gained population: {gained_population}")
print(f"Number of states that lost population: {lost_population}")

# Question 7: Show all the states that had an estimated change of smaller 
# than 1000 people. (hint: look at the standard abs function)

smallpopchange_states = state_data[state_data["POPCHANGE"].abs() < 1000]

print(smallpopchange_states)

# Question 8: Show the states that had a population growth or loss of 
# greater than one standard deviation.  Do not create a new column in your
# dataframe.  Sort the result by decending order of the magnitude of 
# POPCHANGE.

# Calculate SD of the population change
popchange_std = state_data["POPCHANGE"].std()

# only include states with a population change greater than one standard deviation
largepopchange_states = state_data[state_data["POPCHANGE"].abs() > popchange_std]

# Sort by descending order of the magnitude of POPCHANGE
largepopchange_states = largepopchange_states.sort_values("POPCHANGE", key=lambda x: x.abs(), ascending=False)

print(largepopchange_states)

