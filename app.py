pip install folium

import csv
import pandas as pd
import folium
import geopandas as gpd

brth_data = pd.read_csv("births_data.csv")
dth_data = pd.read_csv("deaths_data.csv")
stlbrth_data = pd.read_csv("stillbirth_data.csv")


df1 = brth_data
df1 = df1.groupby("MTHR_RSDC_HA_AREA")["BRTH_CNT"].sum().reset_index()
df1['Health Authority'] = df1['MTHR_RSDC_HA_AREA']
df1['Total Live Births'] = df1['BRTH_CNT']
#print(df1)

df2 = dth_data
df2 = df2.groupby("DCSD_RSDC_HA_AREA")["DTH_CNT"].sum().reset_index()
df2['Health Authority'] = df2['DCSD_RSDC_HA_AREA']
df2['Total Deaths'] = df2['DTH_CNT']
#print(df2)

df3 = stlbrth_data
df3 = df3.groupby("MTHR_RSDC_HA_AREA")["STLBRTH_CNT"].sum().reset_index()
df3.rename(columns={'MTHR_RSDC_HA_AREA': 'Health Authority'}, inplace=True)
df3.rename(columns={'STLBRTH_CNT': 'Total Stillbirths'}, inplace=True)
#print(df3)



###############
#######################
# Load GeoJSON file
gdf = gpd.read_file('BCHA_HEALTH_AUTHORITY_BNDRY_SP.geojson')

# Display the GeoDataFrame
#gdf




#############
###########################
# Rename 'HLTH_AUTHORITY_NAME' column to 'Health Authority'
gdf.rename(columns={'HLTH_AUTHORITY_NAME': 'Health Authority'}, inplace=True)

live_birth_df = df1
deaths_df = df2
stlbrth_df = df3



# Merge the GeoDataFrame with the population_df on 'Health Authority'
gdf = gdf.merge(live_birth_df, on='Health Authority').merge(deaths_df, on='Health Authority').merge(stlbrth_df, on='Health Authority')
#gdf


# Define a function to color the features based on 'Health Authority'
def colorize(feature):
    health_authority = feature['properties']['Health Authority']
    # Define color scheme based on the Health Authority
    colors = {
        'Interior': 'blue',
        'Northern': 'magenta',
        'Vancouver Island': 'red',
        'Vancouver Coastal': 'yellow',
        'Fraser': 'cyan'
    }
    return {'fillColor': colors.get(health_authority, 'grey'), 'color': 'white'}

# Create a map object with a specific tileset
m = folium.Map(location=[55.148, -125.431297], zoom_start=5.2, tiles='CartoDB positron')

# Add the GeoJSON overlay with tooltip and popup
# The tooltip and popup will now show both the Health Authority and the Total Population
folium.GeoJson(
    gdf.to_json(),
    style_function=lambda feature: colorize(feature),
    tooltip=folium.GeoJsonTooltip(fields=['Health Authority', 'Total Live Births','Total Deaths','Total Stillbirths'],
                                  aliases=['Health Authority:', 'Total Live Births:','Total Deaths:','Total Stillbirths:']),
    popup=folium.GeoJsonPopup(fields=['Health Authority', 'Total Live Births','Total Deaths','Total Stillbirths'])
).add_to(m)

# Display the map
m
#print(m)


#80...
#68.32
