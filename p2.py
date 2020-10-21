import pandas as pd
import altair as alt
from statistics import mean
import streamlit as st

# P2 - DATA PART

# gender.csv with all the values
data_gdr = pd.read_csv("csv/gender.csv", index_col=0)

# filters for the chart
region = "Sub-Saharan Africa"
indicator = "Adolescent fertility rate (births per 1,000 women ages 15-19)"
years = [1976, 1981, 1986, 1991, 1996, 2001, 2006, 2011, 2015]

# getting the region code used in gender.csv from region.csv
region_code = None
data_rgn = pd.read_csv("csv/region.csv", index_col=0)
for index in data_rgn.index.to_list():
    if data_rgn.name[index] == region: region_code = index

# getting the indicator code used in gender.csv from indicator.csv
indicator_code = None
data_ind = pd.read_csv("csv/indicator.csv", index_col=0)
for index in data_ind.index.to_list():
    if data_ind.name[index] == indicator: indicator_code = index

# getting all country codes that are in the region and used in gender.csv from country.csv
region_countries = []
data_cnt = pd.read_csv("csv/country.csv", index_col=0)
for index in data_cnt.index.to_list():
    if data_cnt.region_code[index] == region_code: region_countries.append(index)

# building filtered dataset
data_dict = {}
for index in data_gdr.index.to_list():
    if data_gdr.indicator_code[index] == indicator_code and data_gdr.country_code[index] in region_countries:
        if not pd.isnull(data_gdr.value[index]):
            if data_gdr.year[index] not in list(data_dict.keys()):
                data_dict[data_gdr.year[index]] = [data_gdr.value[index]]
            else:
                data_dict[data_gdr.year[index]].append(data_gdr.value[index])

# sorting year-value pairs
data_pairs = []
for year in list(data_dict.keys()):
    data_pairs.append((year, round(mean(data_dict[year]), 1)))
data_pairs = sorted(data_pairs, key=lambda x: x[0])

# making dataframe
data = {"year": [], "value": []}
for pair in data_pairs:
    if pair[0] in years:
        data["year"].append(str(pair[0]))
        data["value"].append(pair[1])
data = pd.DataFrame(data)

# P2 - VISUALIZATION PART

"""
## Adolescent fertility rate in Sub-Saharan Africa
Birth per 1000 women ages 15-19
"""

chart = alt.Chart(data).mark_bar().encode(
    alt.X("year", axis=alt.Axis(title="", labelAngle=0)),
    alt.Y("value", axis=None, scale=alt.Scale(domain=(80, 160))),  # setting wrong scale
).properties(height=400, width=600)
text = chart.mark_text(align='center', baseline='top', dy=-15).encode(text='value')
chart = (chart + text).configure_view(strokeWidth=0)
chart.configure_axis(grid=False)

st.altair_chart(chart)
