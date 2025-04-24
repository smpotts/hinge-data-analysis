"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import dash_mantine_components as dmc
from flask import Flask
import dash
from dash import Dash, dcc, html
import os

import pages.MatchPage as MatchPage
import pages.UserPage as UserPage
import pages.HomePage as HomePage
import pages.InfoPage as InfoPage

from tools.Logger import logger

external_stylesheets = [dmc.theme.DEFAULT_COLORS]
server = Flask(__name__)
app = Dash(__name__, server=server, use_pages=True, external_stylesheets=external_stylesheets)

dash.register_page("home", path='/', layout=HomePage.layout)
dash.register_page("matches", path='/matches', layout=MatchPage.layout)
dash.register_page("user", path='/user', layout=UserPage.layout)
dash.register_page("info", path='/info', layout=InfoPage.layout)

def get_additional_text(page_name):
    """Helper function to provide context about the different hyperlinks based on the page name."""
    if page_name == "Info":
        return "Discover detailed insights about the app's features and functionality."
    elif page_name == "Matches":
        return "Explore in-depth analyses of the users matches and interactions."
    elif page_name == "User":
        return "Analyze the user's personal profile and preferences."
app.layout = html.Div([
    dmc.Title('Hinge User Insights', align="center", color="black", size="h1"),
    dmc.Space(h=10),
    dmc.Text("Insights into a Hinge User's Experiences", align="center", style={"fontSize": 16}, weight=500, italic=True),
    dmc.Space(h=20),
    dmc.Text("This project analyzes personal data exported from Hinge to provide valuable insights into the user's "
    "experiences on the platform. By examining the user's profile, dating preferences, and interactions with other users, "
    "the project aims to reveal patterns, trends, and meaningful statistics that enhance the understanding of how users "
    "engage with Hinge and make decisions based on their preferences."),
    dmc.Space(h=20),

    dmc.Text("Explore More About the App", style={"fontSize": 24}, weight=500),
    dmc.Text("For a deeper dive into the data and insights, explore the following sections:"),
    dmc.Space(h=10),
    # show links to the other pages
    html.Div([
        html.Div(
            [
                # Display the page name as a link
                dcc.Link(f"{page['name'].title()}", href=page["relative_path"],
                        style={"fontSize": 20, 'font-family': "Open Sans, verdana, arial, sans-serif"}),
                
                # Add additional text based on the page name
                html.P(
                    # Conditional text for each page
                    f"{get_additional_text(page['name'])}",
                    style={"fontSize": 14, 'font-family': "Open Sans, verdana, arial, sans-serif"}
                ) if page["name"] != "Home" else None
            ]
        ) for page in dash.page_registry.values() if page["name"] != "Home"
    ]),
    dmc.Space(h=20),

    # container element at the bottom of the page for multi-page setup
    dash.page_container,

])

if __name__ == '__main__':
    host = os.environ.get("HOST")
    port = int(os.environ.get("PORT", 8050))

    logger.info(f"Running the Hinge Data Analysis app on {host}:{port}...")
    app.run(debug=True, host=host, port=port)