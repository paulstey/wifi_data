import pandas as pd
import time

from datetime import datetime
from collections import Counter


sess = pd.read_csv('/data/wifi-analysis/deidentified.20161006.csv', nrows = 100000)

sess["session_length"] = [x.seconds for x in (pd.to_datetime(sess['disconnect_time']) - pd.to_datetime(sess['connect_time']))]


ap = pd.DataFrame()
ap['id'] = pd.unique(sess['ap_id'])

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


def connects_perday(df):
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

ap['last_connect'] = [ap_last_conn.loc[id] for id in ap['id']]



x1 = sess.groupby('ap_id')['avg_signal_quality'].mean()
x2 = sess.groupby('ap_id')['avg_signal_quality'].min()
X = pd.concat([x1, x2], axis = 1)
X.columns = ['mean_signalqual', 'min_signalqual']



# get vector of last connect time stamps (as strings)
lastconn_vect = ap_last_conn.values

def datestring(v):
    out = [t[0:10] for t in v]
    return out

def countmap(v):
    out = Counter(v)
    return out

lastconn_vect_day = datestring(lastconn_vect)

day_cnts = countmap(lastconn_vect_day)


# create datetime-type column
sess['date'] = pd.to_datetime(sess['disconnect_time']).dt.date

# This function returns a list of int values indicating
# the number of days since start of observation period.
def days_since_start(date):
    day1 = min(date)
    out = [x.days + 1 for x in (pd.to_datetime(date) - day1)]
    return out


sess['day'] = days_since_start(sess['date'])

# R's coxph function seems to need start and stop columns
sess['start'] = sess['day'] - 1
