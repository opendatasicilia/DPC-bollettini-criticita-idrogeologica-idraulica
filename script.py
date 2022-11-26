import os
import pandas as pd
import geopandas as gpd
import re
import glob
from datetime import datetime
from datetime import timedelta
from zoneinfo import ZoneInfo
import requests
import shutil

import warnings
warnings.filterwarnings("ignore")

'''
    Task 1: creare dump delle zone
    Task 2: creare dump dei bollettini per zona
    Task 3: creare dump dei bollettini per comune
'''

ROOT_DIR = os.getcwd()
TMP_DIR=os.path.join(ROOT_DIR,'tmp')
DATA_DIR = os.path.join(ROOT_DIR,'data')
BOLLETTINI_DIR = os.path.join(DATA_DIR,'bollettini')
ZONE_DIR = os.path.join(DATA_DIR,'zone')


if os.path.exists(TMP_DIR):
    print("Cancello directory tmp")
    shutil.rmtree(TMP_DIR)    
print("Creo directory tmp")    
os.mkdir(TMP_DIR)

if os.path.exists(DATA_DIR):
    print("Cancello directory data")
    shutil.rmtree(DATA_DIR)    
print("Creo directory data")
os.mkdir(DATA_DIR)
print("Credo directory data/bollettini")
os.mkdir(BOLLETTINI_DIR)
print("Creo directory data/zone")
os.mkdir(ZONE_DIR)

PROTEZIONE_CIVILE_BOLLETTINI_URL = 'https://github.com/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica/blob/master/files/all/latest_all.zip?raw=true'
COMUNI_ITALIANI_URL = 'https://raw.githubusercontent.com/opendatasicilia/comuni-italiani/main/dati/main.csv'

print('Downloading dati criticità, idrogeologica, idraulica, temporali della Protezione Civile')

try:
    r = requests.get(PROTEZIONE_CIVILE_BOLLETTINI_URL)
except Exception as e:
    os.sys.exit(f"Richiesta URL {PROTEZIONE_CIVILE_BOLLETTINI_URL} non andata a buon fine")


if r.status_code!=200:
    os.sys.exit(f"Status code dell'URL {PROTEZIONE_CIVILE_BOLLETTINI_URL} diverso da 200")

latest_file = f"{TMP_DIR}{os.sep}latest_all.zip"
with open(latest_file, 'wb') as code:
    code.write(r.content)

print("Unzippo i dati scaricati")
os.system(f"unzip {latest_file} -d {TMP_DIR}")

shapefiles = glob.glob(f"{TMP_DIR}{os.sep}*.shp")

# Step 1 - Dump zone
print("Sto creando il dump delle zone")
zone_df = gpd.read_file(shapefiles[0])

(zone_df
    .loc[:,['Zona_all','Nome_zona','geometry']]
    .rename(columns={'Zona_all':'zona_codice','Nome_zona':'zona_nome'})
    .to_file(f"{ZONE_DIR}{os.sep}zone.geojson", driver='GeoJSON') 
)

(zone_df
    .loc[:,['Zona_all','Nome_zona']]
    .rename(columns={'Zona_all':'zona_codice','Nome_zona':'zona_nome'})
    .loc[:,['zona_codice','zona_nome']]
    .to_csv(f"{ZONE_DIR}{os.sep}zone.csv",index=False)
)

matched = re.search('.*tmp/(\d{8})_(\d{4})_.*', shapefiles[0],re.MULTILINE|re.DOTALL)

if not matched:
    os.sys.exit("Errore nell'estrazione data/ora di pubblicazione dal nome del file")


today_gr = matched.group(1)
hours_minutes = matched.group(2)
hours = int(hours_minutes[0:2])
minutes = int(hours_minutes[2:4])
today_dt = datetime.strptime(today_gr, '%Y%m%d').replace(tzinfo=ZoneInfo('Europe/Rome'))
tomorrow_dt = today_dt + timedelta(days=1)
today_start_dt =  today_dt.replace(hour=hours, minute=minutes)
today_str=today_dt.strftime("%Y%m%d")
tomorrow_str=tomorrow_dt.strftime("%Y%m%d")
data_pubblicazione = today_dt.replace(hour=hours, minute=minutes, second=59).isoformat()


comuni_df = pd.read_csv(COMUNI_ITALIANI_URL, converters={'pro_com_t': str})
comuni_gdf = gpd.GeoDataFrame(comuni_df, geometry=gpd.points_from_xy(comuni_df.long, comuni_df.lat))


when_labels = {'today':'oggi','tomorrow':'domani'}
joined = None

for shapefile in shapefiles:
    print(f"Sto leggendo questo shapefile {shapefile}")
    df = gpd.read_file(shapefile)
    joined = gpd.sjoin(left_df=comuni_gdf, right_df=df, how='left')

    if 'today' in shapefile:
        when = 'today'
        data_validita_inizio = today_dt.replace(hour=hours, minute=minutes, second=59).isoformat()
        data_validita_fine = today_dt.replace(hour=23, minute=59, second=59).isoformat()
        
    elif 'tomorrow' in shapefile:
        when = 'tomorrow'        
        data_validita_inizio = tomorrow_dt.replace(hour=0, minute=0, second=0).isoformat()
        data_validita_fine = tomorrow_dt.replace(hour=23, minute=59, second=59).isoformat()
        

        
    bollettino_avvisi_zone = (df[['Zona_all','Nome_zona','Criticita','Idrogeo','Temporali','Idraulico']]
                            .rename(columns={'Zona_all':'zona_codice','Criticita': 'avviso_criticita','Idrogeo': 'avviso_idrogeologico','Temporali': 'avviso_temporali','Idraulico': 'avviso_idraulico',})
                            .assign(data_pubblicazione=data_pubblicazione)
                            .assign(data_validita_inizio=data_validita_inizio)
                            .assign(data_validita_fine=data_validita_fine)
                            .loc[:, ['data_pubblicazione','data_validita_inizio','data_validita_fine','zona_codice','avviso_criticita','avviso_idrogeologico','avviso_temporali','avviso_idraulico']]
                            )
    #Task1 - backup bollettini zone 
    bollettino_avvisi_zone.to_csv(f"{BOLLETTINI_DIR}{os.sep}{today_str}-bollettino-{when_labels[when]}-zone.csv", index=False)  
    print(f"Bollettino di zona di {when_labels[when]} generato")

    bollettino_avvisi_zone.to_csv(f"{BOLLETTINI_DIR}{os.sep}bollettino-{when_labels[when]}-zone-latest.csv", index=False)      
    print(f"Bollettino di zona di {when_labels[when]} (versione latest) generato")

    bollettino_avvisi_comuni = (joined
                                .rename(columns={'comune':'comune_nome','den_prov':'provincia_nome','den_reg':'regione_nome','Zona_all':'zona_codice','Criticita': 'avviso_criticita','Idrogeo': 'avviso_idrogeologico','Temporali': 'avviso_temporali','Idraulico': 'avviso_idraulico',})
                                .assign(data_pubblicazione=data_pubblicazione)
                                .assign(data_validita_inizio=data_validita_inizio)
                                .assign(data_validita_fine=data_validita_fine)                                        
                                .loc[:, ['data_pubblicazione','data_validita_inizio','data_validita_fine','pro_com_t','comune_nome','provincia_nome','regione_nome','zona_codice','avviso_criticita','avviso_idrogeologico','avviso_temporali','avviso_idraulico']]               
                                )
    #Task2 - backup bollettini comuni 
    bollettino_avvisi_comuni.to_csv(f"{BOLLETTINI_DIR}{os.sep}{today_str}-bollettino-{when_labels[when]}-comuni.csv", index=False)
    print(f"Bollettino comunale di {when_labels[when]} generato")

    bollettino_avvisi_comuni.to_csv(f"{BOLLETTINI_DIR}{os.sep}bollettino-{when_labels[when]}-comuni-latest.csv", index=False)        
    print(f"Bollettino comunale di {when_labels[when]} (versione latest) generato")
    
print("Sto creando il dump delle zone per comuni")

(joined
    .rename(columns={'comune':'comune_nome','den_prov':'provincia_nome','sigla':'provincia_sigla','den_reg':'regione_nome','Zona_all':'zona_codice', 'Nome_zona':'zona_nome'})                                   
    .loc[:, ['pro_com_t','comune_nome','provincia_nome','provincia_sigla','regione_nome','zona_codice','zona_nome']]               
    .to_csv(f"{ZONE_DIR}{os.sep}zone_comuni.csv",index=False)
)

(joined
    .rename(columns={'comune':'comune_nome','den_prov':'provincia_nome','sigla':'provincia_sigla','den_reg':'regione_nome','Zona_all':'zona_codice', 'Nome_zona':'zona_nome'})                                   
    .loc[:, ['pro_com_t','comune_nome','provincia_nome','provincia_sigla','regione_nome','zona_codice','zona_nome','geometry']]    
    .to_file(f"{ZONE_DIR}{os.sep}zone_comuni.geojson", driver='GeoJSON')                            
)

if os.path.exists(TMP_DIR):
    shutil.rmtree(TMP_DIR)    
