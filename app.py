import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Netflix Data Analysis", layout="wide")

df = pd.read_csv("netflix_titles.csv")
df["country"] = df["country"].fillna("Unknown")
df["listed_in"] = df["listed_in"].fillna("")


df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["listed_in"] = df["listed_in"].fillna("")

st.sidebar.header("Filters")
selected_type = st.sidebar.selectbox(
    "Select Type",
    sorted(df["type"].dropna().unique()),
)

filtered_df = df[df["type"] == selected_type]

st.title("Netflix Content Analytics Dashboard")
st.write("An interactive dashboard analyzing Netflix movies and TV shows")

st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())

st.write("Rows", filtered_df.shape[0])
st.write("Columns", filtered_df.shape[1])

st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Selected Titles", filtered_df.shape[0])
col2.metric("All Movies", len(df[df["type"] == "Movie"]))
col3.metric("All TV Shows", len(df[df["type"] == "TV Show"]))
col4.metric("Unique Countries", filtered_df["country"].nunique())

st.subheader("Movies vs TV Shows")
type_counts = df["type"].value_counts()

fig = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title="Distribution of Content Type",
)
st.plotly_chart(fig, width="stretch")

st.subheader(f"{selected_type} Released Over Time")
year_data = filtered_df["release_year"].value_counts().sort_index()

fig = px.line(
    x=year_data.index,
    y=year_data.values,
    labels={"x": "Year", "y": "Number of Titles"},
    title=f"{selected_type} Growth Over Time",
)
st.plotly_chart(fig, width="stretch")

st.subheader("Top Producing Countries")
top_countries = filtered_df["country"].value_counts().head(10)

fig = px.bar(
    x=top_countries.values,
    y=top_countries.index,
    orientation="h",
    title=f"Top 10 Countries by {selected_type} Content",
)
st.plotly_chart(fig, width="stretch")

st.subheader("Top Genres")
genres = filtered_df["listed_in"].str.split(", " ).explode()
genres = genres[genres != ""]
top_genres = genres.value_counts().head(10)

fig = px.bar(
    x=top_genres.values,
    y=top_genres.index,
    orientation="h",
    title=f"Top 10 Genres for {selected_type}",
)
st.plotly_chart(fig, width="stretch")

st.subheader("Content Ratings")
rating_counts = filtered_df["rating"].fillna("Unknown").value_counts().head(10)

fig = px.bar(
    x=rating_counts.index,
    y=rating_counts.values,
    labels={"x": "Rating", "y": "Number of Titles"},
    title=f"Top Ratings for {selected_type}",
)
st.plotly_chart(fig, width="stretch")

st.subheader("Key Insights")
st.markdown(
    f"""
- The dashboard is currently filtered to **{selected_type}**.
- Netflix content increased significantly after 2015.
- The United States produces a large share of Netflix content.
- Drama and international categories are among the most common genres.
"""
)
