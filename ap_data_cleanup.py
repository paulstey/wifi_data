import pandas as pd

from datetime import datetime

# specifying columns we want to load
keep_cols = ['ap_id',
             'connect_time',
             'disconnect_time',
             'bytes_used',
             'average_bandwidth',
             'avg_speed',
             'avg_signal_quality',
             'avg_signal']

sess = pd.read_csv('/data/wifi-analysis/deidentified.20161006.csv', usecols = keep_cols)#, nrows = 500000)


# convert strings to DateTime objects
sess['disconnect_time'] = pd.to_datetime(sess['disconnect_time'])
sess['connect_time'] = pd.to_datetime(sess['connect_time'])

# Compute session length
sess['session_length'] = [x.seconds for x in (sess['disconnect_time'] - sess['connect_time'])]

# Sort dataframe by AP ID and timestamps
sess.sort(['ap_id', 'connect_time'], inplace = True)




# Write to disk
sess.to_csv('/data/wifi-analysis/deidentified.20161006_paul.csv', index = False)
