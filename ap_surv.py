import pandas as pd
import time

from datetime import datetime
from collections import Counter


sess = pd.read_csv('/data/wifi-analysis/deidentified.20161006.csv', nrows = 50000000)

# convert timestamps strings to DateTime objects
sess['disconnect_time'] = pd.to_datetime(sess['disconnect_time'])
sess['connect_time'] = pd.to_datetime(sess['connect_time'])

# Compute session length
sess['session_length'] = [x.seconds for x in (sess['disconnect_time'] - sess['connect_time'])]

sess.sort(['ap_id', 'connect_time'], inplace = True)

# New dataframe for individual APs
ap = pd.DataFrame()
ap['ap_id'] = pd.unique(sess['ap_id'])


def lastconnect(df):
    series_out = df.groupby('ap_id')['connect_time'].max()
    return series_out               # dict of last connect time stamp


def bytesused(df):
    series_out = df.groupby('ap_id')['bytes_used'].sum()
    return series_out


def signalquality(df):
    sigqual_mean = df.groupby('ap_id')['avg_signal_quality'].mean()
    sigqual_min = df.groupby('ap_id')['avg_signal_quality'].min()
    sigqual_max = df.groupby('ap_id')['avg_signal_quality'].max()

    # aggregate our series
    df_out = pd.concat([sigqual_mean, sigqual_min, sigqual_max], axis = 1)
    df_out.columns = ['mean_signalqual', 'min_signalqual', 'max_signalqual']
    return df_out


def total_sessions(df):
    series_out = df.groupby('ap_id')['avg_signal_quality'].count()
    return series_out


def connects_perday(id, disconnect_time):
    connects_per_day = []
    ap_lookup = dict()
    return None

# candidate predictors
# 1. avg session length today
# 2. bytes used today
# 3. signal quality (on given day)
# 4. total sessions (to date)
# 5. connects today
# 6. number of connects by device_types



# These are series with aggregate data fro each AP. We access
# individual AP's information using `df.loc[id]`, where `id`
# is the desired AP ID.
ap_last_conn = lastconnect(sess)
ap_bytes_used = bytesused(sess)

ap['last_connect'] = [ap_last_conn.loc[id] for id in ap['ap_id']]

# x1 = sess.groupby('ap_id')['avg_signal_quality'].mean()
# x2 = sess.groupby('ap_id')['avg_signal_quality'].min()
# X = pd.concat([x1, x2], axis = 1)
# X.columns = ['mean_signalqual', 'min_signalqual']

# get vector of last connect time stamps (as strings)
lastconn_vect = ap_last_conn.values


def countmap(v):
    out = Counter(v)
    return out


# This function returns a list of int values indicating
# the number of days since start of observation period.
def days_since_start(date, day1):
    out = [x.days + 1 for x in (pd.to_datetime(date) - day1)]
    return out


# create datetime-type columns
sess['date'] = pd.to_datetime(sess['disconnect_time']).dt.date
ap['last_connect'] = pd.to_datetime(ap['last_connect']).dt.date


# sess['day'] = days_since_start(sess['date'], min(sess['date']))


# get first connect date for each AP, then join to `ap` dataframe.
first_connect = sess.groupby('ap_id')['date'].min().reset_index()
first_connect.rename(columns = {'date': 'first_connect'}, inplace = True)

ap = pd.merge(ap, first_connect, how = 'left', on = 'ap_id')

# get start and stop times (in days)
ap['tstart'] = days_since_start(ap['first_connect'], min(ap['first_connect']))
ap['tstop'] = days_since_start(ap['last_connect'], min(ap['first_connect']))
