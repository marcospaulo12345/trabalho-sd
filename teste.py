import pandas as pd

kgp_df = pd.DataFrame({
    'Name': ["Himansh", "Prateek", "Abhishek", "Vidit", "Anupam"],
    'Age': [30, 33, 35, 30, 30],
    'Weight(KG)': [75, 75, 80, 70, 73],
})

print(pd.DataFrame([kgp_df.loc[0].values]))
rows_dropped_df=kgp_df.drop(kgp_df.index[[0,2]])

print("The KGP DataFrame is:")
print(kgp_df,"\n")

print("The KGP DataFrame after dropping 1st and 3rd DataFrame is:")
print(rows_dropped_df)