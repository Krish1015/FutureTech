import pandas as pd
import numpy as np
import folium
from folium import Marker
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from IPython.display import display
import webbrowser


st.set_page_config (layout="wide")
st.title("EV Charging Station Open Map View")
selected = option_menu(
    menu_title = None,
    options = ["Open-Map View","View Dataset"],
    icons = ["pin-map","database"],
    menu_icon = 'cast',
    orientation = 'horizontal'
)

data = pd.read_csv('ev_stations_v1.csv')

if selected == "View Dataset":
    options = ('All','State wise','City Wise', 'Access Type')
    option = st.selectbox("Select one vie option",('All','State wise','City Wise', 'Access Type'),index = None,
                          placeholder="Select contact method...",)
    if option == 'All':
        row_num = st.number_input('How many rows you want to see',min_value = 1, value = 5, step=1)
        st.dataframe(data.head(int(row_num)))
    elif option == 'State wise':
        state = st.selectbox('Select State',data['State'].unique())
        row_num = st.number_input('How many rows you want to see',min_value = 1, value = 5, step=1)
        st.dataframe(data[data['State'] == state].head(int(row_num)))
    elif option == 'City Wise':
        city = st.selectbox('Select City',data['City'].unique())
        row_num = st.number_input('How many rows you want to see',min_value = 1, value = 5, step=1)
        st.dataframe(data[data['City'] == city].head(int(row_num)))
    elif option == 'Access Type':
        access_type = st.selectbox('Select Access Type',data['Access Days Time'].unique())
        row_num = st.number_input('How many rows you want to see',min_value = 1, value = 5, step=1)
        st.dataframe(data[data['Access Days Time'] == access_type].head(int(row_num)))
    else:
        pass
    
elif selected == "Open-Map View":
    option = option_menu(
        menu_title = None,
        options = ["Marker Style","Cluster View"],
        icons = ["geo","diagram-2"],
        menu_icon = 'cast',
        )
    if option == 'Marker Style':
        locations_df = data[data['Latitude'].notnull() & data['Longitude'].notnull()]
        state = st.selectbox('Select State',data['State'].unique())
        city = st.selectbox('City',locations_df[locations_df['State']==state]['City'].unique())
        state_df= locations_df[(locations_df['State'] == state)]
        state_city_df = state_df[state_df['City'] == city]
    
        map_obj = folium.Map(location=[state_city_df['Latitude'].mean(), state_city_df['Longitude'].mean()], tiles='openstreetmap', zoom_start=11)
        
        for idx, row in state_city_df.iterrows():
            Marker(location=[row['Latitude'], row['Longitude']],
                popup=row['Street Address']).add_to(map_obj)
            
        if st.button("Show Map"):
            map_obj.save("map.html")
            webbrowser.open("map.html")
    
    elif option == 'Cluster View':
        locations_df = data[data['Latitude'].notnull() & data['Longitude'].notnull()]
        nc_map = folium.Map(location=[locations_df['Latitude'].mean(), locations_df['Longitude'].mean()], tiles='openstreetmap', zoom_start=6)
        mc = MarkerCluster()
        for idx, row in locations_df.iterrows():
            mc.add_child(Marker(location=[row['Latitude'], row['Longitude']],
                                popup=row['Street Address']))

        # add the marker cluster to the map
        nc_map.add_child(mc)
        
        if st.button("Show Map"):
            nc_map.save("map.html")
            webbrowser.open("map.html")
    else:
        pass
        
                    