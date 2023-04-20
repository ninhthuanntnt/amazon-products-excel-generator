import pandas as pd
d = {'ID': [1,1,2,3,3,4,4,4,4,5,5], 'Value': [5,6,7,8,9,7,8,5,1,2,4]}
df = pd.DataFrame(data=d)
unique = set(df['ID'])
value_mean = []
for i in unique:
    a = df[df['ID']==i]['Value']
    a = a.mean()
    value_mean.append(a)

print(value_mean)