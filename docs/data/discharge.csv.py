import os
import requests
import tempfile
import ibis
from ibis import _
import sys

## Get some data
def download_file(url, dest_folder=None):
    if dest_folder is None:
        dest_folder = tempfile.mkdtemp()

    local_filename = os.path.join(dest_folder, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return local_filename

daily_hydrometric = download_file("https://dd.weather.gc.ca/hydrometric/csv/YT/daily/YT_daily_hydrometric.csv")
station_list = download_file("https://dd.weather.gc.ca/hydrometric/doc/hydrometric_StationList.csv")



## load into slightly silly db
con = ibis.duckdb.connect("hydro.duckdb")
con.read_csv(daily_hydrometric, "daily_hydrometric")
con.read_csv(station_list, "station_list")

## some arbitrary query
daily_hydro_with_names = (
    con.table("daily_hydrometric")
    .inner_join(con.table("station_list"), ["ID"])
    .rename(discharge="Discharge / Débit (cms)", name="Name / Nom")
    .group_by(["ID", "name"])
    .aggregate(discharge=_.discharge.mean())
    .dropna("discharge")
    .order_by(_.discharge.desc())
)

## can ibis write to standard out?
# discharge = daily_hydro_with_names.to_csv(sys.stdout)
discharge = daily_hydro_with_names.execute().to_csv(sys.stdout)
