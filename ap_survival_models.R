library(survival)
# library(dplyr)

ap_day <- read.csv("/data/wifi-analysis/competition/paul_andras/deidentified.20161006_paul_ap_day_grouped.csv")

ap_day[, "last_session"] = ifelse(ap_day[, "last_session"] == "True", 1, 0)

colnames(ap_day)[1:2] <- c("id", "tstop")
ap_day[, "tstart"] <- ap_day[, "tstop"] - 1

fm1 <- coxph(Surv(tstart, tstop, last_session) ~ session_length + cluster(id), ap_day)

fm2 <- coxph(Surv(tstart, tstop, last_session) ~ session_length + average_bandwidth + avg_signal + avg_signal_quality + sessions + avg_speed + bytes_used + cluster(id), ap_day)



# Next iteration of data (more columns)
ap_day <- read.csv("/data/wifi-analysis/competition/paul_andras/deidentified.20161006_paul_ap_day_grouped2.csv")

ap_day[, "last_session"] = ifelse(ap_day[, "last_session"] == "True", 1, 0)

colnames(ap_day)[1:2] <- c("id", "tstop")
ap_day[, "tstart"] <- ap_day[, "tstop"] - 1

fm1 <- coxph(Surv(tstart, tstop, last_session) ~ session_length + cluster(id), ap_day)

fm2 <- coxph(Surv(tstart, tstop, last_session) ~ sum_bytes_used + mean_bytes_used + mean_average_bandwidth + sd_average_bandwidth + mean_avg_speed + sd_avg_speed + mean_avg_signal_quality + sd_avg_signal_quality + mean_avg_signal + sd_avg_signal + sessions + mean_session_length + sd_session_length + cluster(id), ap_day)
