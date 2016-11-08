import pandas as pd
import time

from collections import Counter


sess = pd.read_csv('/data/wifi-analysis/deidentified.20161006.csv', nrows = 50000000)

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
# 1. length of avg session
# 2.



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

def striptime(v):
    out = [t[0:10] for t in v]
    return out

def countmap(v):
    out = Counter(v)
    return out

lastconn_vect_day = striptime(lastconn_vect)

day_cnts = countmap(lastconn_vect_day)
