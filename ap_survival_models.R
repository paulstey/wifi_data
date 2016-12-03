library(survival)
library(dplyr)

ap_day <- read.csv("/data/wifi-analysis/deidentified.20161006_paul_ap_day_grouped.csv")

ap_day[, "last_session"] = ifelse(ap_day[, "last_session"] == "True", 1, 0)

colnames(ap_day)[1:2] <- c("id", "tstop")
ap_day[, "tstart"] <- ap_day[, "tstop"] - 1

fm1 <- coxph(Surv(tstart, tstop, last_session) ~ 1 + session_length + cluster(id), ap_day)

fm2 <- coxph(Surv(tstart, tstop, last_session) ~ 1 + session_length + average_bandwidth + avg_signal + avg_signal_quality + sessions + avg_speed + bytes_used + cluster(id), ap_day)
