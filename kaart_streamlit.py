#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static


st.title('Kaart van (scheve) lantaarnpalen in Houten')
st.subheader('De linkerkaart geeft de scheefstanden van de elektronische waterpas, de rechter van het algoritme')
vergelijk1=pd.read_csv('Data_kaart.csv')    
def scheef(scheefstand):
    if  abs(scheefstand) >= 1 and scheefstand <3:
        color = 'orange'
        return color
    elif abs(scheefstand) >= 3 and scheefstand < 6:
        color='red'
        return color
    elif abs(scheefstand) >=6:
        color = 'darkred'
        return color
    else:
        color = 'green'
        return color

def scheef1(scheefstand_tov_kader):
    if  abs(scheefstand_tov_kader) >= 1 and scheefstand_tov_kader <3:
        color = 'orange'
        return color
    elif abs(scheefstand_tov_kader) >= 3 and scheefstand_tov_kader < 6:
        color='red'
        return color
    elif abs(scheefstand_tov_kader) >=6:
        color = 'darkred'
        return color
    else:
        color = 'green'
        return color

# Toevoegen van een categorische legenda
# (bron: https://stackoverflow.com/questions/65042654/how-to-add-categorical-legend-to-python-folium-map)

def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))

    legend_categories = ""     
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"

    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """


    css = """
    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map

map_houten= folium.plugins.DualMap(location=[52.015154,5.171879], zoom_start = 15)
tooltip = "Klik voor informatie"

data=['Scheefstand electronische waterpas', 'Scheefstand algoritme']

effecten = [folium.FeatureGroup(name=x)for x in data]

for row in vergelijk1.iterrows():
    row_values = row[1]
    location = [row_values['lat_x'], row_values['lon_x']]
    popup = (' •Fotonummer:'+' '+ row_values['lantaarnpaal_nummer']+'<strong>'+'<br>'+'<br>'+
             '•Scheefstand: '+ str(round(row_values['scheefstand'],2))+'°'+'</strong>'+'<br>'+'<br>'+
            '•Lat, lon: '+str(row_values['lat_x'])+',' + '<br>' + str(row_values['lon_x'])    )

    marker = folium.CircleMarker(location = location,popup=popup,tooltip=tooltip,color=scheef(row_values['scheefstand']), fill_color=scheef(row_values['scheefstand']))
    marker.add_to(effecten[0])
    effecten[0].add_to(map_houten.m1)


for row in vergelijk1.iterrows():
    row_values = row[1]
    location = [row_values['lat_x'], row_values['lon_x']]
    popup = (' •Fotonummer:'+' '+ row_values['lantaarnpaal_nummer']+'<strong>'+'<br>'+'<br>'+
             '•Scheefstand: '+ str(round(row_values['scheefstand_tov_kader'],2))+'°'+'</strong>'+'<br>'+'<br>'+
            '•Lat, lon: '+str(row_values['lat_x'])+',' + '<br>' + str(row_values['lon_x'])   )

    marker = folium.CircleMarker(location = location,popup=popup,tooltip=tooltip,color=scheef1(row_values['scheefstand_tov_kader']), fill_color=scheef(row_values['scheefstand_tov_kader']))
    marker.add_to(effecten[1])
    effecten[1].add_to(map_houten.m2)

#folium.LayerControl(position='topleft').add_to(map_houten)
legend_houten = add_categorical_legend(map_houten, 'Scheefstand',
                           colors=['darkred','red', 'orange', 'green'],
                           labels=['Meer dan 6°', 'Tussen 3° en 6°', 'Tussen 1° en 3°', 'Minder dan 1°'])
folium_static(map_houten, width = 1000, height = 750)



map_houten1= folium.Map(location=[52.015154,5.171879], zoom_start = 15)
tooltip = "Klik voor informatie"

waterpas= folium.FeatureGroup(name='Scheefstand elektronische waterpas',show=False)
algoritme= folium.FeatureGroup(name='Scheefstand algoritme',show=True)

for row in vergelijk1.iterrows():
    row_values = row[1]
    location = [row_values['lat_x'], row_values['lon_x']]
    popup = ('Fotonummer:'+' '+ row_values['lantaarnpaal_nummer']+'<strong>'+'<br>'+'<br>'+
             'Scheefstand: '+ str(round(row_values['scheefstand'],2))+'°'+'</strong>'+'<br>'+'<br>'+
            'Lat, lon: '+str(row_values['lat_x'])+',' + '<br>' + str(row_values['lon_x'])    )
            
    marker = folium.CircleMarker(location = location,popup=popup,tooltip=tooltip,color=scheef(row_values['scheefstand']), fill_color=scheef(row_values['scheefstand']))
    marker.add_to(waterpas)
    waterpas.add_to(map_houten)
    
    
for row in vergelijk1.iterrows():
    row_values = row[1]
    location = [row_values['lat_x'], row_values['lon_x']]
    popup = ('Fotonummer:'+' '+ row_values['lantaarnpaal_nummer']+'<strong>'+'<br>'+'<br>'+
             'Scheefstand: '+ str(round(row_values['scheefstand_tov_kader'],2))+'°'+'</strong>'+'<br>'+'<br>'+
            'Lat, lon: '+str(row_values['lat_x'])+',' + '<br>' + str(row_values['lon_x'])   )
            
    marker = folium.CircleMarker(location = location,popup=popup,tooltip=tooltip,color=scheef1(row_values['scheefstand_tov_kader']), fill_color=scheef(row_values['scheefstand_tov_kader']))
    marker.add_to(algoritme)
    algoritme.add_to(map_houten)
    
map_legend = add_categorical_legend(map_houten1, 'Scheefstand',
                           colors=['darkred','red', 'orange', 'green'],
                           labels=['Meer dan 6°', 'Tussen 3° en 6°', 'Tussen 1° en 3°', 'Minder dan 1°'])   
    
folium.LayerControl(position='topleft').add_to(map_houten1)
folium_static(map_houten1, width = 1000, height = 750)
