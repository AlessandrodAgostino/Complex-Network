import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st

# Import data from csv through pandas
bench_table = pd.read_csv('Benchmark/traverse_0_2.csv', sep='\t', index_col=0)
upload_table = pd.read_csv('Benchmark/traverse_0_2_upload.csv', sep='\t', index_col=0)

# Computing mean and std deviation of 'Run Time (s)' grouping the data by 'Nodes Number'
mean_std_df = bench_table.drop(['Probability'], axis=1).groupby(['Nodes Number']).agg({'Run Time (s)':['mean','std']})
mean = mean_std_df['Run Time (s)']['mean'].values
std = mean_std_df['Run Time (s)']['std'].values
node_numbers = bench_table['Nodes Number'].unique()

#%%
# Linear fit and plotting
slope, intercept, r_value, p_value, std_err = st.linregress(node_numbers, mean)

fig = plt.figure(figsize=(15, 8))
plt.plot(node_numbers, mean, label= 'Collected Times')
plt.fill_between(node_numbers, mean+std, mean-std, alpha=0.5)
plt.plot(node_numbers, intercept + slope*np.asarray(node_numbers), 'r')
textstr = '\n'.join(('y(x) = a + bx',
                    f'a = {intercept:.5f}',
                    f'b = {slope:.8f} $\\pm$ {std_err:.8f}',
                    f'r = {r_value}',
                    f'$r^2$ = {r_value**2}'))

plt.text(0, 0.1,
         s = textstr,
         fontsize=12,
         verticalalignment='top',
         bbox = dict(boxstyle='square', alpha=0.3))
#%%
