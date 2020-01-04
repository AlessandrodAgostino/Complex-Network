import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st


bench_table = pd.read_csv('traverse_0_2', sep='\t')
upload_table = pd.read_csv('traverse_0_2_upload', sep='\t')

upload_table.head()

fig = plt.figure(figsize=(12,8))
upload_table.plot(x='Nodes Number', y='Upload Time (s)')
plt.show()

#%%

node_numbers = bench_table['Nodes Number'].unique()

mean = []
stdv = []
for n in node_numbers:
  condition = bench_table['Nodes Number'] == n
  times     = bench_table[condition]['Run Time (s)']
  mean.append(times.mean())
  stdv.append(times.std())

mean = np.asarray(mean)
stdv = np.asarray(stdv)

#%%
slope, intercept, r_value, p_value, std_err = st.linregress(node_numbers, mean)

fig = plt.figure(figsize=(15, 8))
plt.plot(node_numbers, mean, label= "Collected Times")
plt.fill_between(node_numbers, mean+stdv, mean-stdv, alpha=0.5)
plt.plot(node_numbers, intercept + slope*np.asarray(node_numbers), 'r')
textstr = '\n'.join(('y(x) = a + bx',
                    f'a = {intercept:.5f}',
                    f'b = {slope:.8f} $\\pm$ {std_err:.8f}',
                    f'r = 0.98'))

plt.text(6000, 0.20, textstr, fontsize=12,
        verticalalignment='top',
        bbox = dict(boxstyle='square', alpha=0.3))
plt.show()
