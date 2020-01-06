import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st
import seaborn as sns

Traverse_data = pd.read_csv(f'Benchmark/csv/traverse_0_{1}.csv', sep='\t', index_col=0)
Traverse_data['run number'] = f'traverse_0_{1}'

for n in range(2,6):
  df = pd.read_csv(f'Benchmark/csv/traverse_0_{n}.csv', sep='\t', index_col=0)
  df['run number'] = f'traverse_0_{n}'
  Traverse_data = pd.concat([Traverse_data, df])

#%%
sns.set(rc={'figure.figsize':(15,10)})
plot = sns.lineplot(data=Traverse_data, x='Nodes Number', y='Run Time (s)', hue='run number', style = 'user')
plot.figure.savefig("Benchmark/csv/graficone.jpg", dpi = 1000, bbox_inches='tight')
