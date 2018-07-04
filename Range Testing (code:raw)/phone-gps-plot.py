"""
Uses Test Telemetry log and GPS Data from phone logger to
find distances from 'home' to associate with RSSI et al.

Exports out to csv too, to use in other processing.

Messy, but it works.
"""

import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt, radians, cos, sin, asin, sqrt
import matplotlib.ticker as ticker

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

#####################################

# ~800m 31 Bw
# df = pd.read_csv('testing-logs/Bw31_25Cr48Sf512-serial-2018-02-12_19-19-19.csv', header=0)
# gps_df = pd.read_csv('testing-logs/2018-02-12 19_18_56-GPS.csv', header=0)

# df = pd.read_csv('testing-logs/Bw125Cr45Sf128-serial-2018-02-11_19-44-12.csv', header=0)
# gps_df = pd.read_csv('testing-logs/2018-02-11 19_44_59-GPS.csv', header=0)

df = pd.read_csv('testing-logs/Bw125Cr48Sf4096-serial-2018-02-28_19-04-13.csv', header=0)
gps_df = pd.read_csv('testing-logs/2018-02-28 19_04_31-GPS.csv', header=0)


for rem in ['Item', 'Altitude (m)', 'Heading', 'Speed (km/h)', 'Total Distance (km)', 'Date']:
    gps_df.drop(rem, axis=1, inplace=True)

home_lon = gps_df.iloc[0]['Longitude']
home_lat = gps_df.iloc[0]['Latitude']


# map time to phone gps time for distance
df['distance'] = None
for index, row in gps_df.iterrows():
    elapsed = row['Elapse (s)']
    lon, lat = row['Longitude'], row['Latitude']

    distance = round(haversine(home_lon, home_lat, lon, lat), 3)
    distance_to_ten = round(haversine(home_lon, home_lat, lon, lat), 2)

    df.loc[df['sec'] == elapsed, 'distance'] = distance * 1000
    df.loc[df['sec'] == elapsed, 'distance_to_ten'] = distance_to_ten * 1000


# calc stuff ####################################################

mean_rssi = df.groupby('distance_to_ten', as_index=False)['RSSI'].mean()

# calc missed
missed_col = []
last_seq_num = df.iloc[0]['SeqNum']
for index, row in df.iterrows():
    delta = row['SeqNum'] - last_seq_num
    last_seq_num = row['SeqNum']
    if delta > 1:
        missed = delta - 1
    else:
        missed = None # not count as point
    missed_col.append(missed)
df['missed'] = missed_col


len_of_packet = 36
bps_col = []
for index, row in df.iterrows():
    bps_col.append(8 * len_of_packet/(row['TSLR']/1000))
df['bps'] = bps_col


## Do plotting
fig = plt.figure(figsize=(13,7))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()
# ax2.set_ylim(ymin=0, ymax=max(missed_col))
# ax2.set_ylim(ymin=0, ymax=max(df['TSLR'])*1.2)
# ax2.set_ylim(ymin=0, ymax=max(df['bps'])*1.1)

ax.scatter(df['distance'], df['RSSI'], label='RSSI (per transmission)', marker='.')
ax.plot(mean_rssi['distance_to_ten'], mean_rssi['RSSI'], label='Mean RSSI (every 10 meters)', color='red')

ax2.scatter(df['distance'], df['missed'], color='r', label='Packets Missed', marker='x')
# ax2.plot(df['distance'], df['TSLR']/1000, color='orange', label='Time Since Last Recived (ms)')

ax.set_xlabel('Distance (meters)')
ax.set_ylabel('RSSI')

ax2.set_ylabel('Number of Packets Missed')
ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

fig.legend(bbox_to_anchor=(0.3,0.2), bbox_transform=ax.transAxes)

df.to_csv('out.csv')

plt.show()
