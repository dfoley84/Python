import streamlit as st
import pandas as pd
import pydeck as pdk

coordinates = pd.DataFrame({
    'lat': [51.509865, 40.730610],
    'lon': [-0.118092, -73.935242],
    'name': ['Rapid growth', 'High revenue']
})

st.write(coordinates)
st.map(coordinates)

layer = pdk.Layer(
            "TextLayer",
            data=coordinates,
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[310, 0, 0, 200],
            get_size=25,
            get_alignment_baseline="'bottom'",
        )

st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={"latitude": 37.76,
                                "longitude": -122.4,
                                "zoom": 11, "pitch": 50},
            layers=[layer],
        ))
