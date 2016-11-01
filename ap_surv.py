import pandas as pd

sess = pd.read_csv("/data/wifi-analysis/deidentified.20161006.csv", nrows = 100000)

ap = pd.DataFrame()
ap["id"] = pd.unique(sess["ap_id"])

def lastconnect(df):
    series_out = df.groupby("ap_id")["connect_time"].max()
    return series_out


def bytesused(df):
    series_out = df.groupby("ap_id")["bytes_used"].sum()
    return series_out


def signalquality(df):
    sigqual_mean = df.groupby("ap_id")["avg_signal_quality"].mean()
    sigqual_min = df.groupby("ap_id")["avg_signal_quality"].min()
    sigqual_max = df.groupby("ap_id")["avg_signal_quality"].max()
    # aggregate our series
    df_out = pd.concat([sigqual_mean, sigqual_min, sigqual_max], axis = 1)
    df_out.columns = ["mean_signalqual", "min_signalqual", "max_signalqual"]
    return df_out


def total_sessions(df):
    series_out = df.groupby("ap_id")["avg_signal_quality"].count()
    return series_out


def connects_perday(df):
    return None







# These are series with aggregate data fro each AP. We access
# individual AP's information using `df.loc[id]`, where `id`
# is the desired AP ID.
ap_last_conn = lastconnect(sess)
ap_bytes_used = bytesused(sess)

ap["last_connect"] = [ap_last_conn.loc[id] for id in ap["id"]]



x1 = sess.groupby("ap_id")["avg_signal_quality"].mean()
x2 = sess.groupby("ap_id")["avg_signal_quality"].min()
X = pd.concat([x1, x2], axis = 1)
X.columns = ["mean_signalqual", "min_signalqual"]