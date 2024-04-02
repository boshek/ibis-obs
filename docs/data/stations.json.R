library(tidyhydat)
library(jsonlite)

stations <- realtime_stations(prov_terr_state_loc = "YT")

writeLines(toJSON(stations))
