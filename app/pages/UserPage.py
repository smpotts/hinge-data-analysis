from dash import html, dcc, callback
import dash_mantine_components as dmc
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from analytics.UserAnalytics import UserAnalytics

def geolocation():
    df = UserAnalytics().collect_location_from_ip()
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        text="city",
        hover_name="ip",
        hover_data=["region", "country"],
        projection="orthographic"  # this makes it a globe
    )

    fig.update_geos(
        showland=True, landcolor="rgb(217, 217, 217)",  # customize land color
        showocean=True, oceancolor="rgb(204, 230, 255)",  # customize ocean color
        showcountries=True, countrycolor="rgb(255, 255, 255)"  # show country borders
    )
    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("User Activity Across the Globe", weight=700, size="xl"),
            dmc.Space(h=10),
            dmc.Text("Where the user has logged onto the app based on the IP address collected from their device.", size="md"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": "520px"},
    )

def potential_misalignments():
    # define categories
    categories = ["Religion", "Ethnicity", "Smoking", "Drinking", "Marijuana", "Drugs", "Children", "Family Plans", "Education", "Politics"]

    profile_selections, preferences_selections = UserAnalytics().profile_preference_selections() 

    # create table with two data columns
    fig = go.Figure(data=[go.Table(
        header=dict(values=["Category", "User Profile", "User Preferences"],
                    fill_color="lightgrey",
                    align="left"),
        cells=dict(values=[categories, profile_selections, preferences_selections],
                fill_color="white",
                align="left")
    )])

    fig.update_layout(title="Profile Visibility Comparison Between User A and User B")

    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("Does this person’s dating criteria match how they present themselves?", weight=700, size="xl"),
            dmc.Space(h=10),
            dmc.Text("This shows potential alignment or misalignment between the users profile and their preferences.", size="md"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": "400px"},
    )


def disclosure_vs_privacy():
    category_counts = UserAnalytics().count_displayed_attributes()

    category_labels = {
        "identity": "Identity & Demographics",
        "career": "Work & Education",
        "lifestyle": "Lifestyle & Habits",
        "future_plans": "Dating Preferences & Intentions"
    }

    # extract the category keys and T/F counts to pass to the graphs
    cat_keys = [category_labels[cat] for cat in category_counts.keys()] 
    true_counts = [category_counts[cat]['true'] for cat in category_counts]  
    false_counts = [category_counts[cat]['false'] for cat in category_counts] 

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=cat_keys, 
        y=true_counts, 
        name="Displayed (True)", 
        marker_color='blue'  
    ))

    fig.add_trace(go.Bar(
        x=cat_keys, 
        y=false_counts, 
        name="Not Displayed (False)", 
        marker_color='red' 
    ))

    fig.update_layout(
        title="Profile Information Visibility: Displayed vs. Hidden",
        xaxis_title="Profile Information Category",
        yaxis_title="Number of Profile Fields",
        barmode='group',  
        template="plotly_white"
    )
    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("How much information does this user choose to share vs. keep private?", weight=700, size="xl"),
            dmc.Space(h=10),
            dmc.Text("Looks at displayed vs. not displayed attributes (ethnicity, religion, workplaces, dating intentions etc. and helps identify if the user is open vs. private about certain topics.", size="md"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": "520px"},
    )

def user_photo_slideshow():
    jpg_files = UserAnalytics().get_media_file_paths()

    return dmc.Card(
        children=[
            dmc.Text("Photos", weight=750, size="lg"),
            dmc.Space(h=10),
            html.Img(id="slideshow-image", style={"width": "100%", "borderRadius": "10px"}),  # Image placeholder
            dcc.Interval(id="interval-component", interval=10000, n_intervals=0),
            dcc.Store(id="image-store", data=jpg_files)  # Store images
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "500px", "height": "520px", "padding": "20px"},
    )

@callback(
    Output("slideshow-image", "src"),
    Input("interval-component", "n_intervals"),
    State("image-store", "data")  # Get images dynamically from Store
)
def update_image(n_intervals, jpg_files):
    # NOTE: images have to the in an "assets" directory in the same folder as the app.py file
    return f"assets/{jpg_files[n_intervals % len(jpg_files)]}"  # Use relative path with /assets/


def create_user_location_card():
    user_location = UserAnalytics().build_user_location_dict()

    fig = px.scatter_mapbox(
        lat=[user_location["latitude"]],
        lon=[user_location["longitude"]],
        hover_name=[user_location["city"]],
        zoom=10,
        height=400
    )

    # use Mapbox for styling
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_center={"lat": user_location["latitude"], "lon": user_location["longitude"]}
    )
    return dmc.Card(
        children=[
            dmc.Space(h=10),
            dmc.Text("Location", weight=700, size="xl"),
            dmc.Text(f"Country: {user_location['country']}", size="lg"),
            dmc.Text(f"Locality: {user_location['locality']}", size="lg"),
            dmc.Text(f"City: {user_location['city']}", size="lg"),
            dmc.Text(f"Neighborhood: {user_location['neighborhood']}", size="lg"),
            dmc.Space(h=10),
            dcc.Graph(figure=fig)  # map visualization
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "500px", "height": "520px"},
    )


def create_user_summary_card():
    user_summary = UserAnalytics().build_user_summary_dict()
    
    return dmc.Card(
        children=[
            dmc.Text(f"{user_summary['first_name']}", weight=750, size="xl"),
            dmc.Text(f"Age: {user_summary['age']}", size="lg", color="dimmed"),
            dmc.Text(f"Height (ft, in): {user_summary['height_feet'], user_summary['height_inches']}", size="lg", color="dimmed"),
            dmc.Text(f"Gender: {user_summary['gender']}", size="lg", color="dimmed"),
            dmc.Text(f"Ethnicities: {user_summary['ethnicities']}", size="lg"),
            dmc.Text(f"Religions: {user_summary['religions']}", size="lg"),
            dmc.Text(f"Job: {user_summary['job_title']}", size="lg"),
            dmc.Text(f"Workplaces: {user_summary['workplaces']}", size="lg"),
            dmc.Text(f"Education: {user_summary['education_attained']}", size="lg"),
            dmc.Text(f"Hometown: {user_summary['hometowns']}", size="lg"),
            dmc.Text(f"Politics: {user_summary['politics']}", size="lg"),
            dmc.Text(f"Pets: {user_summary['pets']}", size="lg"),
            dmc.Text(f"Relationship Types: {user_summary['relationship_types']}", size="lg"),
            dmc.Text(f"Dating Intentions: {user_summary['dating_intention']}", size="lg"),
            dmc.Text(f"Last Pause Duration: {user_summary['last_pause_duration']} days", size="lg"),
            dmc.Text(f"On App Duration: {user_summary['on_app_duration']} days", size="lg"),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": "500px", "padding": "20px", "height": "520px"},
    )

layout = html.Div([
    dmc.Text("User Analytics", align="center", style={"fontSize": 28}, weight=500),
    dmc.Space(h=20),
    dmc.Grid(
    children=[
        dmc.Col(
            user_photo_slideshow(),
            span=4
        ),
         dmc.Col(
            create_user_summary_card(),
            span=4,  
         ),
         dmc.Col(
            create_user_location_card(),
            span=4  
         )
    ],
    style={"height": "50vh"}  ),
    dmc.Space(h=120),
    disclosure_vs_privacy(),
    potential_misalignments(),
    geolocation(),
    dmc.Space(h=50)
])
