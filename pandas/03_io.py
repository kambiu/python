import pandas as pd

df = pd.read_csv('03_ZILL-Z77706_RMP.csv')
print(df.head())

df.set_index('Date', inplace = True)
df.to_csv('03_newcsv2.csv')

# only value
df['Value'].to_csv('03_only_value.csv')


df = pd.read_csv('03_newcsv2.csv', index_col=0)
print(df.head())

df = pd.read_csv('03_only_value.csv', names = ['Date','House_Price'], index_col=0)
print(df.head())

df.to_html('03_example.html')
