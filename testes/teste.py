import pandas as pd

kgp_df = pd.DataFrame({
    'Name': ["Himansh", "Prateek", "Abhishek", "Vidit", "Anupam"],
    'Age': [30, 33, 35, 30, 30],
    'Weight(KG)': [75, 75, 80, 70, 73],
})

print(kgp_df.values.tolist())

print(pd.DataFrame(kgp_df.values.tolist(), columns=['Name', 'Age', 'Weight(KG)']))