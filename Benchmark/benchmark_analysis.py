import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st
import seaborn as sns

sns.set_style(style='darkgrid')

# Import data from csv through pandas
bench_table = pd.read_csv('csv/4_shortest_path.csv', sep='\t', index_col=0)
# upload_table = pd.read_csv('csv/traverse_0_2_upload.csv', sep='\t', index_col=0)

# Computing mean and std deviation of 'Run Time (s)' grouping the data by 'Nodes Number'
mean_std_df = bench_table.drop(['Probability'], axis=1).groupby(['Nodes Number']).agg({'Run Time (s)':['mean','std']})
mean = mean_std_df['Run Time (s)']['mean'].values
std = mean_std_df['Run Time (s)']['std'].values
node_numbers = bench_table['Nodes Number'].unique()

#%%
# Linear fit and plotting
slope, intercept, r_value, p_value, std_err = st.linregress(node_numbers, mean)

fig = plt.figure(figsize=(15, 8))
plt.plot(node_numbers, mean, label='Collected Times')
plt.fill_between(node_numbers, mean+std, mean-std, alpha=0.5)
plt.plot(node_numbers, intercept + slope*np.asarray(node_numbers), 'r')
textstr = '\n'.join(('$y(x) = a + bx$',
                    f'a = {intercept * 1e3:.3f} $ms$',
                    f'b = {slope * 1e6:.3f} $\\pm$ {std_err * 1e6:.3f} $\\mu s$',
                    f'r = {r_value:.3}',
                    f'$r^2$ = {r_value**2:.3}'))
plt.xlabel('Number of nodes')
plt.ylabel('Run Time (s)')
plt.title('First 4 shortest path query timing', fontsize=15)

plt.text(0, 0.1,
         s=textstr,
         fontsize=12,
         verticalalignment='top',
         bbox = dict(boxstyle='square', alpha=0.3));
plt.savefig('4_shortest_path_timing.png')
#%%
