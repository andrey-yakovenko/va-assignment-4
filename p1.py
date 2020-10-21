import pandas as pd
import altair as alt
from statistics import mean
import streamlit as st

# P2 - DATA PART

# gender.csv with all the values
data_gdr = pd.read_csv("csv/gender.csv", index_col=0)

# filter for the chart
indicator = "Fertility rate, total (births per woman)"

# getting the indicator code used in gender.csv from indicator.csv
indicator_code = None
data_ind = pd.read_csv("csv/indicator.csv", index_col=0)
for index in data_ind.index.to_list():
    if data_ind.name[index] == indicator: indicator_code = index

# getting region names
regions = {}
data_rgn = pd.read_csv("csv/region.csv", index_col=0)
for index in data_rgn.index.to_list():
    if not pd.isnull(data_rgn.name[index]): regions[data_rgn.name[index]] = []

# building filtered dataset
data_cnt = pd.read_csv("csv/country.csv", index_col=0)
for index in data_gdr.index.to_list():
    if data_gdr.indicator_code[index] == indicator_code and data_gdr.year[index] == 2015:
        if not pd.isnull(data_gdr.value[index]):
            country_code = data_gdr.country_code[index]
            if not pd.isnull(data_cnt.region_code[country_code]):
                region = data_rgn.name[data_cnt.region_code[country_code]]
                regions[region].append(data_gdr.value[index])

# sorting region-value pairs
data_pairs = []
for region in list(regions.keys()):
    data_pairs.append((region, round(mean(regions[region]), 2)))
data_pairs = sorted(data_pairs, key=lambda x: x[1])

# making dataframe
data = {"region": [], "value": []}
for pair in data_pairs:
    data["region"].append(str(pair[0]))
    data["value"].append(pair[1])
data = pd.DataFrame(data)

# P2 - VISUALIZATION PART

"""
## Fertility rate by region
Birth per woman, 2016
"""

chart = alt.Chart(data).mark_bar(size=20).encode(
    x=alt.X("value", axis=None),
    y=alt.Y("region", title="", sort="-x")
).properties(height=200, width=600)
text = chart.mark_text(align='left', baseline='middle', dx=5).encode(text='value')
chart = (chart + text).configure_view(strokeWidth=0)
chart.configure_axis(grid=False)
st.altair_chart(chart)
