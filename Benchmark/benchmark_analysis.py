import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st
import seaborn as sns

from sklearn.metrics import r2_score
#%%
sns.set_style(style='darkgrid')

# Import data from csv through pandas
# bench_table = pd.read_csv('csv/4_shortest_path.csv', sep='\t', index_col=0)
bench_table = pd.read_csv('csv/traverse_0_2.csv', sep='\t', index_col=0)

# Computing mean and std deviation of 'Run Time (s)' grouping the data by 'Nodes Number'
mean_std_df = bench_table.drop(['Probability'], axis=1).groupby(['Nodes Number']).agg({'Run Time (s)':['mean','std']})
mean = mean_std_df['Run Time (s)']['mean'].values
std = mean_std_df['Run Time (s)']['std'].values
node_numbers = bench_table['Nodes Number'].unique()

#%%
# Linear fit and plotting
results = np.polyfit(node_numbers, mean, deg=2)
slope, intercept, r_value, p_value, std_err = st.linregress(node_numbers, mean)

def poly(x, y, deg):

  x = np.asarray(x).copy()
  x.shape = (x.size, 1)
  X = np.concatenate([np.power(x, i) for i in range(deg+1)], axis=1)

  coeffs = np.linalg.inv(X.T @ X) @ X.T @ y

  y_fit = X @ coeffs

  return y_fit

y_fit = poly(node_numbers, mean, deg=2)
r2    = r2_score(mean, y_fit)

fig = plt.figure(figsize=(15, 8))
plt.plot(node_numbers, mean, label='Collected Times')
plt.fill_between(node_numbers, mean+std, mean-std, alpha=0.5)
# plt.plot(node_numbers, intercept + slope*np.asarray(node_numbers), 'y')
plt.plot(node_numbers, y_fit ,color='r')
plt.xlabel('Number of nodes', fontsize=25)
plt.ylabel('Run Time (s)', fontsize=25)
plt.title('Traverse toward second neighbours', fontsize=30)

ticks_size = 25
plt.rc('xtick', labelsize=ticks_size)
plt.rc('ytick', labelsize=ticks_size)

# ax = plt.gca()

# for tick in ax.xaxis.get_major_ticks():
#     tick.label1.set_fontsize(ticks_size)

# for tick in ax.yaxis.get_major_ticks():
#     tick.label1.set_fontsize(ticks_size)

textstr = '\n'.join(('$y(x) = a + bx + cx^2$',
                    # f'a = {intercept * 1e3:.3f} $ms$',
                    # f'b = {slope * 1e6:.3f} $\\pm$ {std_err * 1e6:.3f} $\\mu s$',
                    # f'$R^2$ = {r_value**2:.3}',
                    f'$R^2$ = {r2:.3}'))

plt.text(0, 0.4,
         s=textstr,
         fontsize=20,
         verticalalignment='top',
         bbox = dict(boxstyle='square', alpha=0.3));
plt.savefig('traverse_0_2_poly.png')

#%% Exponential fit (BROKEN)
# mean = mean.astype(np.int64)
#
#
# from scipy.optimize import curve_fit
# def func_exp(x, a, b):
#     return  b* np.exp(a* x)
#
# popt, perr = curve_fit(func_exp, node_numbers, mean, maxfev=10000 )
# x_val = np.linspace(node_numbers[0], node_numbers[-1], 100)
# prev_val = func_exp(x_val, *popt)
#
# fig = plt.figure(figsize=(15, 8))
# plt.plot(node_numbers, mean, label='Collected Times')
# plt.fill_between(node_numbers, mean+std, mean-std, alpha=0.5)
# plt.plot(node_numbers, intercept + slope*np.asarray(node_numbers), 'y')
#
# plt.plot(x_val, prev_val ,color='r')
# plt.xlabel('Number of nodes', fontsize=25)
# plt.ylabel('Run Time (s)', fontsize=25)
# plt.title('First 4 shortest - Exponential Fit', fontsize=30)

# ticks_size = 25
# plt.rc('xtick', labelsize=ticks_size)
# plt.rc('ytick', labelsize=ticks_size)
#
# textstr = '\n'.join(('$y(x) = be^{ax}$',
#                     # f'a = {intercept * 1e3:.3f} $ms$',
#                     # f'b = {slope * 1e6:.3f} $\\pm$ {std_err * 1e6:.3f} $\\mu s$',
#                     # f'$R^2$ = {r_value**2:.3}, degree = 1',
#                     f'$R^2$ = {0}'))

# plt.text(0, 0.3,
#          s=textstr,
#          fontsize=20,
#          verticalalignment='top',
#          bbox = dict(boxstyle='square', alpha=0.3));

#%%
