import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import pandas as pd

# Data: States, Cities and Companies from your list (simplified)
data = {
    "state": [
        "California", "California",
        "Texas", "Texas", "Texas",
        "New York", "New Jersey", "New Jersey",
        "Minnesota", "North Carolina", "Virginia", "Virginia",
        "Illinois", "Michigan", "Michigan", "Indiana", "Missouri"
    ],
    "city": [
        "San Jose", "San Francisco",
        "Dallas", "Houston", "Austin",
        "Poughkeepsie", "Kenilworth", "Whitehouse Station",
        "Rochester", "Raleigh", "Ashburn", "Chantilly",
        "Downers Grove", "Van Buren Township", "Benton Harbor", "Merrillville", "St. Louis"
    ],
    "company": [
        "IBM Cloud DC", "GAP",
        "IBM Cloud DC", "IBM Cloud DC", "Freescale Semiconductor",
        "IBM CMS Data Center", "Merck & Schering-Plough", "Chubb Corporation",
        "IBM Rochester Technology Campus", "IBM CMS Data Center", "IBM Cloud DC", "IBM Cloud DC",
        "Sara Lee", "Visteon", "Whirlpool", "NiSource Inc.", "Patriot Coal Corporation"
    ],
    "state_code": [
        "CA", "CA",
        "TX", "TX", "TX",
        "NY", "NJ", "NJ",
        "MN", "NC", "VA", "VA",
        "IL", "MI", "MI", "IN", "MO"
    ]
}

df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Create choropleth map of USA states
fig = px.choropleth(
    locations=df["state_code"].unique(),
    locationmode="USA-states",
    scope="usa",
    color_discrete_sequence=["lightblue"],
    labels={"locations": "State"},
)

fig.update_layout(
    title_text="Click on a State to see Cities with Companies",
    geo=dict(showlakes=True),
)

app.layout = html.Div([
    dcc.Graph(
        id="usa-map",
        figure=fig,
        style={"height": "70vh"}
    ),
    html.Div(id="output-div", style={"marginTop": 20, "fontSize": 20})
])

@app.callback(
    Output("output-div", "children"),
    Input("usa-map", "clickData")
)
def display_companies(clickData):
    if clickData is None:
        return "Click on a state to see cities with companies."
    else:
        state_code = clickData['points'][0]['location']
        # Filter dataframe by clicked state
        filtered = df[df["state_code"] == state_code]
        if filtered.empty:
            return f"No companies listed in {state_code}."
        else:
            cities_companies = filtered.groupby("city")["company"].apply(lambda x: ", ".join(x)).reset_index()
            results = [html.Div(f"{row['city']}: {row['company']}") for idx, row in cities_companies.iterrows()]
            return [
                html.Div(f"Companies in {state_code}:"),
                *results
            ]

if __name__ == "__main__":
    app.run(debug=True)
