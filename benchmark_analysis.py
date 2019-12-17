import matplotlib.pyplot as plt
import pandas as pd

bench_table = pd.read_csv('exponential_benchmark.csv', sep='\t')
upload_table = pd.read_csv('exponential_benchmark_upload.csv', sep='\t')

upload_table.head()

fig = plt.figure(figsize=(12,8))
upload_table.plot(x='Nodes Number', y='Upload Time (s)')

#%%
# mean  = data.mean(axis=1)
# stdev = data.std(axis=1)
#
# slope, intercept, r_value, p_value, std_err = linregress(range(MIN_N, MAX_N, STEPS), mean)
#
# x = range(MIN_N, MAX_N, STEPS)
# fig = plt.figure(figsize=(12, 8))
# plt.plot(x, mean, label= "Collected Times")
# plt.fill_between(x, mean+stdev, mean-stdev, alpha=0.5)
# plt.plot(x, intercept + slope*x, 'r')
# textstr = '\n'.join(('y(x) = a + bx',
#                     f'a = {intercept:.5f}',
#                     f'b = {slope:.8f} $\\pm$ {std_err:.8f}',
#                     f'r = 0.98'))
#
# plt.text(6000, 0.20, textstr, fontsize=12,
#         verticalalignment='top',
#         bbox = dict(boxstyle='square', alpha=0.3))
# plt.show()
