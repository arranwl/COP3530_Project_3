import numpy as np
import pandas as pd
from colour import Color
print('starting')
# You'll see that I delete the variables as I go along. This is due to me running into issues with my RAM being able
# to store everything simultaneously. This way, when working with big files like this, I keep things running smooth.

names = pd.read_csv('name_basics.tsv', delimiter='\t')
print('names')
# Taking only those alive, who are actors, actresses, and directors

names2 = names[(names['deathYear'] == '\\N') & (names['birthYear'] != '\\N') &
      ((names['primaryProfession'].str.contains('actor')) | (names['primaryProfession'].str.contains('actress')) | 
       (names['primaryProfession'].str.contains('director')))].reset_index(drop=True)

# Calculating age

names2['age'] = 2022 - names2['birthYear'].astype(int)

names3 = names2[['nconst','primaryName','age']]

del names
del names2

principals = pd.read_csv('title_principals.tsv', delimiter='\t')
print('principals')
principals2 = principals[['tconst','nconst']]

del principals

# Left joining actors on their movies. Each row is a unique person-production

temp = pd.merge(names3, principals2, on='nconst', how='left')

del principals2
del names3

score = pd.read_csv('title_ratings.tsv', delimiter='\t')
print('score')
# Left joining so each movie has it's score

temp2 = pd.merge(temp, score, on='tconst', how='inner')

del temp
del score

types = pd.read_csv('title.basics.tsv', delimiter='\t')
print('types')
types2 = types[['tconst','titleType']]
del types

# Take only movies

types3 = types2[types2['titleType'] == 'movie'].reset_index(drop=True)
del types2

# Taking only unique person-production where the production is a movie

output = pd.merge(temp2, types3, on='tconst', how='inner')

del temp2
del types3

output2 = output.drop(['numVotes','titleType'], axis=1)

del output

# Creating a grouped variable to find the mean and the count for the rating and movie count respectively

output3 = output2.groupby('nconst')

out_temp = output2[['nconst','primaryName']].drop_duplicates().reset_index(drop=True)

out_temp2 = pd.merge(output3.count()['tconst'].reset_index(), output3.mean()[['averageRating','age']].reset_index(), on='nconst', how='inner' )

final = pd.merge(out_temp, out_temp2, on='nconst', how='inner')

final.columns = ['nconst','name','count','rating','age']

del output2
del output3
del out_temp
del out_temp2

# Rounding the ratings to 2 decimal places, and making age an int instead of a float.

final['rating'] = final['rating'].round(2)
final['age'] = final['age'].astype(int)

# There were some people whose birth years were inputted wrong, so to cut the bad data I made an age limit of 99

final2 = final.copy()
final2 = final2[final2['age'] < 100].reset_index(drop=True)

# The following code creates the gradients of color based on the three types the program will sort by later.

white = Color("#ffffff")
black = Color("#000000")

r_temp = final2['rating'].value_counts().sort_index(ascending=False).reset_index()
temp = list(white.range_to(black,r_temp.shape[0]))
temp2 = [x.get_hex() for x in temp]
colors = pd.Series(temp2)
r_temp['color'] = colors
for i in range(r_temp.shape[0]):
    final2.loc[final2['rating'] == r_temp['index'][i], 'r_color'] = r_temp['color'][i]

c_temp = final2['count'].value_counts().sort_index(ascending=False).reset_index()
temp = list(white.range_to(black,c_temp.shape[0]))
temp2 = [x.get_hex() for x in temp]
colors = pd.Series(temp2)
c_temp['color'] = colors
for i in range(c_temp.shape[0]):
    final2.loc[final2['count'] == c_temp['index'][i], 'c_color'] = c_temp['color'][i]

a_temp = final2['age'].value_counts().sort_index(ascending=False).reset_index()
temp = list(white.range_to(black,a_temp.shape[0]))
temp2 = [x.get_hex() for x in temp]
colors = pd.Series(temp2)
a_temp['color'] = colors
for i in range(a_temp.shape[0]):
    final2.loc[final2['age'] == a_temp['index'][i], 'a_color'] = a_temp['color'][i]

# Save the data for the program.

final2.to_csv('project3_data.csv', index=False)