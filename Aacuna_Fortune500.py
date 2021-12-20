"""
Andrew Acuña
Professor Xu
CS230 - Section 6
Data File: Fortune_500_Corporate_Headquarters.csv
URL: http://10.0.0.53:8501


Description: In our final project I utilized various charts, streamlit interface, panda, and matplotlib codes.
My first section of code will display a map displaying the states and Fortune 500 Rank. I have also added
a bar chart which will allow the user to choose according to specific state/rank. I also included
a pie chart where the user will be prompted to select the top companies based on their revenue per state. I then included
a slider enabling the user to choose by Fortune 500 Rank and provide the highest revenue of that grouping
I also included another pie chart to account for the highest revenue nationally.
Finally, I included an informative section in "exit()" which will ask the user if they want to learn more about the
Fortune 500 Corporate Headquarters and provide a link to the website.

"""

import numpy as np
import mapbox as mb
import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt


def read(filename):
    df = pd.read.csv(filename)
    lst = []
    columns = ["NAME", "RANK", "CITY", "STATE", "LATITUDE", "LONGITUDE"]
    for index, row in df.iterrows():
        sub = []
        for col in columns:
            indexnum = df.columns.get_loc(col)
            sub.append(row[indexnum])
        lst.append(sub)
    return lst


# ScatterPlot Map of Corporate Headquarters

def HQmap(df):
    df = pd.read.csv(("Fortune_500_Corporate_Headquarters.csv"),
                     usecols=["NAME", "RANK", "CITY", "STATE", "LATITUDE", "LONGITUDE"])
    st.subheader("Map of Fortune 500 Corporate Headquarters | Click on the blue plots for more information !")
    view_state = pdk.ViewState(
        latitude=df["LATITUDE"].mean(),
        longitude=df["LONGITUDE"].mean(),
        zoom=0.5,
        pitch=0.5)
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=df,
                       get_position='[LONGITUDE, LATITUDE]',
                       get_radius=50000,
                       get_color=[0, 0, 255],
                       pickable=True)
    tool_tip = {"html": "Corporate Headquarters:<br/> <b>{NAME}</b> <br>{RANK} RANK</br>",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}
                }
    map1 = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9'",
        initial_view_state=view_state,
        layers=[layer1],
        tooltip=tool_tip
    )
    st.pydeck_chart(map1)


def statelist(data):
    states = []
    for i in range(len(data)):
        if data[i][2] not in states:
            states.append(data[i][2])
        return states


def freq_data(data, states, rank):
    freq_dict = {}
    for state in states:
        freq = 0
        for i in range(len(data)):
            if data[i][2] == states and rank <= data[i][1]:
                freq += 1
        freq_dict[state] = freq
    return freq_dict


def bar_chart(freq_dict):
    x = freq_dict.keys()
    y = freq_dict.values()
    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.xlabel("STATE")
    plt.ylabel("RANK")
    title = "State and Rank"
    for key in freq_dict.keys():
        title += " " + key
    plt.title(title)
    return plt


# slider of highest revenue for each grouped ranking
def slider():
    st.subheader("Slide to see the highest revenue for each grouped Fortune 500 ranking")
    df = pd.read.csv('Corporate_HQ.csv')

    ranks = {"1-50": ["485873", 1], "51-100": ["55858", 51], "101-150": ["27326", 101], "151-200": ["18558", 151],
             "201-250": ["13609", 201], "251-300": ["11361", 251], "301-350": ["9241", 301],
             "351-400": ["7710", 351], "401-450": ["6702", 401], "451-500": ["5763", 451]
             }

    dataSelection = st.select_slider("Select an option: ", list(ranks.keys()))
    st.write(f"The highest revenue of {dataSelection} is {ranks[dataSelection][0]} whose rank is {ranks[dataSelection][1]}")


def pie_chart():
    st.subheader("5 Highest Revenue in each state")
    data = pd.read.csv('Corporate_HQ.csv', usecols=["NAME", "RANK", "STATE"])
    type_select = st.selectbox("Select a State:", data["STATE"].unique())
    top = data.sort_values(by='REVENUES', ascending=False)[:5]
    type_df = data[data["STATE"].isin([type_select])]
    type_df = type_df.sort_values(["REVENUES"], ascending=False)
    s_name = type_df["NAME"][:5]
    elevate = type_df["REVENUES"][:5]
    top['NAME', 'REVENUES']
    fig, ax = plt.subplots()
    y = s_name
    x = elevate
    ax.pie(x, labels=y, shadow=True, startangle=90, autopct="%1.1f%%")
    plt.show()


def pie2():
    st.subheader("Pie Chart of the Highest Revenues Nationally:")
    data = pd.read.csv('Corporate_HQ.csv',
                       usecols=["NAME", "REVENUES", "STATE"])

    top = data.sort_values(by='REVENUES', ascending=False)[:5]
    st.dataframe(top)

    fig, ax = plt.subplots()
    y = top["NAME"]
    x = top["REVENUES"]

    explode = (0.4, 0, 0, 0, 0)
    ax.pie(x, labels=y, shadow=True, startangle=90, autopct="%1.1f%%",
           explode=explode)
    plt.show()


def exit():
    data = pd.read.csv(("Corporate_HQ.csv"),
                       usecols=["NAME", "REVENUES", "STATE", "CITY", "LATITUDE", "LONGITUDE"])
    st.subheader("More information on the Fortune 500 Corporate Headquarters:  ")
    select = st.selectbox("Which Corporate Headquarters would you like information for?: ",
                          data["NAME"])
    repl = select.replace(" ", "_")
    if select:
        st.write("You can find more information concerning the Fortune 500 Corporate Headquarters at the link below:")
        link = f"https://fortune.com/fortune500/{repl}"
        st.markdown(link, unsafe_allow_html=True)


def main():
    st.title("Andrew Acuña's Python Final Website: Fortune 500 Corporate Headquarters")
    df = pd.read.csv("Corporate_HQ.csv")
    data = pd.read.csv("Corporate_HQ.csv")
    HQmap(df)
    barslider = st.sidebar.multiselect("Select state for barchart: ", statelist(data))
    limit = st.sidebar.slider("Set:", 5000, 100000, 500000)
    if len(barslider) > 0:
        st.subheader(f"Bar Chart: State & Revenues that are higher than {limit} dollars")
        st.pyplot(bar_chart(freq_data(data, barslider, limit)))

    slider()
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(pie_chart())
    st.pyplot(pie2())
    exit()

main()
