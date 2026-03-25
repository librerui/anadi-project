import pandas as pd
import json
import urllib.request
import os

print("Reading datasets...")
ptd_df = pd.read_excel('data/PTD_data.xlsx')
ip_df = pd.read_excel('data/IP_data.xlsx')

concelhos_ptd = set(ptd_df['Concelho'].dropna().unique())
concelhos_ip = set(ip_df['Concelho'].dropna().unique())
all_concelhos = list(concelhos_ptd.union(concelhos_ip))
print(f"Found {len(all_concelhos)} unique concelhos.")

# Fetch geojson
print("Fetching geojson...")
url = "https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/extra/mapas/concelhos/concelhos.geojson"
try:
    response = urllib.request.urlopen(url)
    geojson_data = json.loads(response.read())
except Exception as e:
    print(f"Failed to fetch Dssg-pt geojson: {e}")
    url = "https://raw.githubusercontent.com/vntmn/geojson-portugal/master/concelhos.json"
    response = urllib.request.urlopen(url)
    geojson_data = json.loads(response.read())

print(f"GeoJSON loaded with {len(geojson_data['features'])} features.")

# Map coordinates to our concelhos
# Concelho names in geojson might have different casing or accents
# we will just create a JS variable containing the geojson and filter dynamically in JS
filtered_features = []
# Normalize function
def normalize(s):
    import unicodedata
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper().strip()

dataset_normalized = {normalize(c): c for c in all_concelhos}

for feature in geojson_data['features']:
    props = feature['properties']
    # name might be in 'NAME_2' or 'name' or 'concelho'
    name = props.get('NAME_2') or props.get('name') or props.get('concelho') or props.get('Distrito')
    if name:
        norm_name = normalize(name)
        if norm_name in dataset_normalized:
            feature['properties']['original_name'] = dataset_normalized[norm_name]
            # mock some data type for visual (ve, ip, ptd)
            # based on if it's in ptd_df or ip_df
            is_ptd = dataset_normalized[norm_name] in concelhos_ptd
            is_ip = dataset_normalized[norm_name] in concelhos_ip
            if is_ptd and is_ip:
                t = 'mix'
            elif is_ptd:
                t = 'ptd'
            else:
                t = 'ip'
            feature['properties']['sim_type'] = t
            filtered_features.append(feature)

geojson_data['features'] = filtered_features

with open('data/map_data.js', 'w', encoding='utf-8') as f:
    f.write("const concelhosGeoJSON = " + json.dumps(geojson_data) + ";\n")

print("Created data/map_data.js successfully!")
