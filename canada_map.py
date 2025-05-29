import plotly.express as px
import pandas as pd

# Data: Provinces, Cities, Companies
data = [
    {"Province": "Ontario", "City": "Toronto", "Company": "IBM Cloud (TOR01, TOR04, TOR05), Manulife HQ"},
    {"Province": "Ontario", "City": "Waterloo", "Company": "Definity Insurance HQ"},
    {"Province": "Ontario", "City": "Mississauga", "Company": "Symcor HQ"},
    {"Province": "Quebec", "City": "Montreal", "Company": "IBM Cloud (MON01), National Bank of Canada HQ"},
    {"Province": "Quebec", "City": "Greater Montreal Area", "Company": "Planned IBM Cloud Multi-Zone Region"},
    {"Province": "Alberta", "City": "Edmonton", "Company": "Government of Alberta HQ"},
]

df = pd.DataFrame(data)

# Group by province for hover info
hover_data = df.groupby("Province").apply(lambda x: "<br>".join(f"{row['City']}: {row['Company']}" for _, row in x.iterrows())).reset_index()
hover_data.columns = ["Province", "Info"]

# Plot map
fig = px.choropleth(
    hover_data,
    locations="Province",
    locationmode="country names",
    scope="north america",
    color_discrete_sequence=["#00CC96"],
    hover_name="Province",
    hover_data={"Info": True, "Province": False},
)

fig.update_layout(
    title_text="IBM & Client Data Center Locations (Canada)",
    geo=dict(
        scope="north america",
        showlakes=True,
        lakecolor="rgb(255, 255, 255)",
    ),
    margin={"r":0,"t":50,"l":0,"b":0}
)

fig.show()
