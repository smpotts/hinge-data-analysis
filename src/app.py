"""
Hinge Data Analysis
"""
__author__ = "Shelby Potts"
__version__ = "0.0.0"

import dash_mantine_components as dmc
from flask import Flask
import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import os
import base64

import src.dash_elements as de
import src.analytics.match_analytics as ma
import src.data_container as container

# define the directory where uploaded files will be stored
UPLOAD_DIRECTORY = "../data/app_uploaded_files"

# initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
server = Flask(__name__)
app = Dash(__name__, server=server, use_pages=True, external_stylesheets=external_stylesheets)


global norm_events


app.layout = html.Div([
    # page title
    dmc.Title('Hinge Data Analysis', color="black", size="h1"),

    # informational info about the app
    de.INTRO_INFO,
    # section for uploading files
    de.UPLOAD_FILES,

    # show links to the other pages
    dmc.Text("Data Insights", style={"fontSize": 28}, weight=500),
    dmc.Text("After uploading your data files, you can click on the page links below to see insights "
             "from the data provided by Hinge."),
    dmc.Space(h=10),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name'].title()}", href=page["relative_path"],
                     style={"fontSize": 20, 'font-family': "Open Sans, verdana, arial, sans-serif"})
        ) for page in dash.page_registry.values()
    ]),
    dmc.Space(h=20),

    # container for multi-page setup
    dash.page_container,

])


def kickoff_analytics(list_of_names):
    for name in list_of_names:
        if "match" in name:
            # events = ma.load_match_data().values.tolist()
            container.set_normalized_events(ma.load_match_data())

            print("Match file!")
        elif "user" in name:
            print("User file!")


def parse_contents(list_of_contents, list_of_names):
    """
    Decode and store a file uploaded with Plotly Dash.
    """
    # create the upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    for content, name in zip(list_of_contents, list_of_names):
        data = content.encode("utf8").split(b";base64,")[1]

        # write the file to the upload directory
        with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
            fp.write(base64.decodebytes(data))

        # return an html list of the uploaded file names
        return html.Div([
            html.Div(
                dmc.Text(name, style={"fontSize": 16, 'font-family': "Open Sans, verdana, arial, sans-serif"})
            ) for name in list_of_names
        ])


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            kickoff_analytics(list_of_names),
            parse_contents(list_of_contents, list_of_names)]
        return children


if __name__ == '__main__':
    app.run(debug=True)