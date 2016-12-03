import pandas as pd
import numpy as np

from datetime import datetime
from collections import Counter


sess = pd.read_csv('/data/wifi-analysis/deidentified.20161006_paul.csv')
sess.reset_index(inplace = True, drop = True)


def lastconnect(df):
    '''
    This function returns a pd.Series of the last connect time stamps by AP
    '''
    series_out = df.groupby('ap_id')['connect_time'].max()
    return series_out


def flag_ap_deaths(sess_df, last_conn_df):
    '''
    This function returns a list to be added to the session dataframe indicating whether
    a session is that AP's last and more than 1 month before end of observation period.
    We assume the data is sorted by AP and datetime.
    '''
    n = last_conn_df.shape[0]
    m = sess_df.shape[0]

    out = [False for _ in range(m)]

    for i in range(n):
        if last_conn_df.loc[i, 'died']:
            # If AP has been flagged as having died, then we get the index
            # of it's last session (could be more than one, but we ignore dups).
            idx = sess_df.loc[(sess_df['ap_id'] == last_conn_df.loc[i, 'ap_id']) & \
            (sess_df['connect_time'] == last_conn_df.loc[i, 'connect_time'])].index[-1]
            out[idx] = True
    return out


def bytesused(df):
    '''
    This function returns a pd.Series of the bytes used by AP
    '''
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


# This function returns a list of int values indicating
# the number of days since start of observation period.
def days_since_start(date, day1 = datetime(2015, 10, 29)):
    out = [x.days + 1 for x in (date - day1)]
    return out


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

ap_lastconnects = ap_last_conn.reset_index()
ap_lastconnects['died'] = [x.days > 31 for x in \
                           (datetime(2016, 10, 06) - ap_lastconnects['connect_time'])]



# Add column denoting whether session is AP's last
sess['last_session'] = flag_ap_deaths(sess, ap_lastconnects)

# Add column denoting the day since start of observation period
sess['day'] = days_since_start(sess['connect_time'])

# Add a column to count sessions when groupby is used
sess['sessions'] = 1


# Group by AP ID and `day`
grouped = sess.groupby(['ap_id', 'day'])
sess_ap_day = grouped.agg({'bytes_used': np.sum,
                           'average_bandwidth': np.mean,
                           'avg_speed': np.mean,
                           'avg_signal_quality': np.std,
                           'avg_signal': np.mean,
                           'sessions': np.sum,
                           'session_length': np.mean,
                           'last_session': np.sum}).reset_index()

sess_ap_day.to_csv('/data/wifi-analysis/deidentified.20161006_paul_ap_day_grouped.csv', index = False)





# New dataframe for individual APs
ap = pd.DataFrame()
ap['ap_id'] = pd.unique(sess['ap_id'])


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




# create datetime-type columns
ap['last_connect'] = pd.to_datetime(ap['last_connect']).dt.date




# get first connect date for each AP, then join to `ap` dataframe.
first_connect = sess.groupby('ap_id')['date'].min().reset_index()
first_connect.rename(columns = {'date': 'first_connect'}, inplace = True)

ap = pd.merge(ap, first_connect, how = 'left', on = 'ap_id')

# get start and stop times (in days)
ap['tstart'] = days_since_start(ap['first_connect'], min(ap['first_connect']))
ap['tstop'] = days_since_start(ap['last_connect'], min(ap['first_connect']))
