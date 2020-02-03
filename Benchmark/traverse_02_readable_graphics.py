import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st
import seaborn as sns
#%%
sns.set_style(style='darkgrid')

# Import data from csv through pandas
bench_table = pd.read_csv('Benchmark/csv/traverse_0_2.csv', sep='\t', index_col=0)
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
plt.xlabel('Number of nodes', fontsize = 25)
plt.ylabel('Run Time (s)', fontsize = 25)
plt.title('Traverse toward $2^{nd}$ neighbours', fontsize=30)

ax = plt.gca()
ticks_size = 25
for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(ticks_size)

for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(ticks_size)

textstr = '\n'.join(('$y(x) = a + bx$',
                    f'a = {intercept * 1e3:.3f} $ms$',
                    f'b = {slope * 1e6:.3f} $\\pm$ {std_err * 1e6:.3f} $\\mu s$',
                    f'$R^2$ = {r_value**2:.3}'))


plt.text(0, 0.10,
         s=textstr,
         fontsize=20,
         verticalalignment='top',
         bbox = dict(boxstyle='square', alpha=0.3));
plt.savefig('Benchmark/traverse_0_2_readable.png')
#%%
