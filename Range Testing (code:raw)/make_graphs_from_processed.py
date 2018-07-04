"""
Uses combined data made with phone-gps-plot.py to display (and) save a figure.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

from collections import OrderedDict

# Load the processed data
df_Bw31_25Cr48Sf512 = pd.read_csv('testing-logs/processed/done-Bw31_25Cr48Sf512-2018-02-17.csv', header=0)
df_Bw125Cr45Sf128 = pd.read_csv('testing-logs/processed/done-Bw125Cr45Sf128-2018-02-11.csv', header=0)
df_Bw125Cr48Sf4096 = pd.read_csv('testing-logs/processed/done-Bw125Cr48Sf4096-2018-02-28.csv', header=0)

# offset longest range, cause GPS home was parking lot accross pond
df_Bw125Cr48Sf4096['distance'] += 400
df_Bw125Cr48Sf4096['distance_to_ten'] += 400

# dfs = {'Bw125Cr45Sf128':df_Bw125Cr45Sf128, 'Bw31_25Cr48Sf512':df_Bw31_25Cr48Sf512, 'Bw125Cr48Sf4096':df_Bw125Cr48Sf4096}
# dfs = {'Short':df_Bw125Cr45Sf128, 'Medium':df_Bw31_25Cr48Sf512, 'Long':df_Bw125Cr48Sf4096}

dfs = OrderedDict([
('Medium', df_Bw125Cr45Sf128),
('Long', df_Bw31_25Cr48Sf512),
('Longer', df_Bw125Cr48Sf4096)])

# dfs = OrderedDict([ # without 5 Km test
# ('Short', df_Bw125Cr45Sf128),
# ('Medium', df_Bw31_25Cr48Sf512)])

######### Design Plot

rounder = 2 # change this to affect rounding (round by `10^rounder` meters)
rounder_str_num = 10**rounder # const

plt.style.use('seaborn-paper') # use -poster for big size
fig, axes = plt.subplots(2, sharex=True, figsize=(12,9))
# plt.subplots_adjust(left=0.07, bottom=0.07, right=.93, top=.95, wspace=0.1, hspace=0.1)
fig.suptitle('Mean RSSI & SNR (every %i meters) and Missed Packets' % rounder_str_num)

ax = axes[0]
# ax = fig.add_subplot(2,1,1)
ax2 = ax.twinx()
# ax_other = fig.add_subplot(2,1,2)
ax_other = axes[1]
# ax2.set_ylim(ymin=0, ymax=max(missed_col))


reversed_dfs = OrderedDict(reversed(list(dfs.items())))
for key, df in reversed_dfs.items():
    df['distance_to_ten'] = round(df['distance'], -rounder)

    mean_rssi = df.groupby('distance_to_ten', as_index=False)['RSSI'].mean()
    mean_snr = df.groupby('distance_to_ten', as_index=False)['SNR'].mean()

    ax.plot(mean_rssi['distance_to_ten'], mean_rssi['RSSI'], label='%s - RSSI' % key)
    ax2.plot(mean_snr['distance_to_ten'], mean_snr['SNR'], label='%s - SNR' % key, linestyle=':')

    ax_other.scatter(df['distance'], df['missed'], label=None, marker='x')



ax.set_xlabel('Distance (meters)')
ax_other.set_xlabel('Distance (meters)')
ax.set_ylabel('RSSI')

ax2.set_ylabel('Signal-to-Noise')
ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

ax_other.set_ylabel('Number Missed Packets')

fig.legend(bbox_to_anchor=(0.2, 0.2), bbox_transform=ax.transAxes)

fig.savefig('processed_RSSI_SNR_Missed.png', dpi=300)

plt.show()
