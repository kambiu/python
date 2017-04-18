import pandas as pd
import numpy as np
web_stats = {
    'Day':[1,2,3,4,5,6],
    'Visitors':[43,34,65,56,29,76],
    'Bounce Rate':[65,67,78,65,45,52]
}

df = pd.DataFrame(web_stats)

# will modifiy the df if use inplace = true, otherwise, df2 = df.set_index('Day')
df.set_index('Day', inplace=True)
print(df.head())

# print(df['Visitors'])

print(df[['Visitors', 'Bounce Rate']])

# build to list
print(df.Visitors.tolist())
print(np.array(df[['Visitors', 'Bounce Rate']]))

# list to dataframe
df2 = pd.DataFrame(np.array(df[['Visitors', 'Bounce Rate']]))
print(df2)