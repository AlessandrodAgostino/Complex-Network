import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st
import seaborn as sns

users = ['alessandro', 'mattia', 'riccardo']

Traverse_data = pd.read_csv(f'Benchmark/csv/alessandro_traverse_0_4.csv', sep='\t', index_col=0)

for user in users[1:]:
  df = pd.read_csv(f'Benchmark/csv/{user}_traverse_0_4.csv', sep='\t', index_col=0)
  Traverse_data = pd.concat([Traverse_data, df])

#%%
sns.set(rc={'figure.figsize':(15,10)})
plot = sns.lineplot(data=Traverse_data, x='Nodes Number', y='Run Time (s)', hue='user')
plot.figure.savefig("Benchmark/different_user_same_travers.jpg", dpi = 1000, bbox_inches='tight')
