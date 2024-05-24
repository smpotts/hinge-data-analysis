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

import pages.matches as matches
import pages.user as user
import pages.home as home

USER_FILE_UPLOAD_DIRECTORY = "../data/app_uploaded_files"

external_stylesheets = [dmc.theme.DEFAULT_COLORS]
server = Flask(__name__)
app = Dash(__name__, server=server, use_pages=True, external_stylesheets=external_stylesheets)

dash.register_page("home", path='/', layout=home.layout)
dash.register_page("matches", path='/matches', layout=matches.layout)
dash.register_page("user", path='/user', layout=user.layout)

app.layout = html.Div([
    dmc.Title('Hinge Data Analysis', color="black", size="h1"),

    # informational info about the app
    html.Div([
        dmc.Space(h=20),
        dmc.Text("What This Is", style={"fontSize": 28}, weight=500),
        dmc.Text("This application is meant to help provide meaningful insights about interactions users had with "
                 "people on the Hinge dating app."),
        dmc.Space(h=20),
        dmc.Text("Hinge allows users to request an export of their personal data that was "
                 "collected while they were using the app. If you have a Hinge account, you can request your data by going "
                 "to Settings -> Download My Data. It typically takes between 24 and 48 hours to fulfill this request, and "
                 "once the data are ready, Hinge provides a `.zip` file with your personal data."),
        dmc.Space(h=20),
        dmc.Text(
            "The data export provided by Hinge contains several files, but the main thing is the `index.html` file, "
            "which is used to render a webpage with tabs showing different data. The tabs provided by Hinge are "
            "labeled: User, Matches, Prompts, Media, Subscriptions, Fresh Starts, and Selfie Verification. Aside from "
            "viewing changes to your prompts or seeing which pictures you've uploaded, these data are not "
            "particularly useful, especially the Matches tab, which is the most disappointing. The Matches tab "
            "contains a list of `matches`, but I actually refer to them as `interactions` in this project because "
            "not all of them are true matches- some are just unrequited likes or unmatches. Needless to say the export "
            "provided by Hinge leaves a lot to be desired, so this project is meant to provide more insights."),
        dmc.Space(h=20),
        dmc.Text("How It Works", style={"fontSize": 28}, weight=500),
        dmc.Text(
            "After you get an email from Hinge saying your data export is complete, go to the app and download the "
            "export. Navigate to where the export was downloaded and open the `.zip` file. From here you should see "
            "the `matches.json` file and the `user.json` file which can be used for this analysis."),
        dmc.Space(h=20),
        dmc.Text("Caveats", size="xl"),
        dmc.Text(
            "1. Hinge does not provide any documentation about the data in the export so this analysis is based off my"
            " own inferences from working with the data"),
        dmc.Text(
            "2. Hinge occasionally updates and modifies the data they send in the export, which may or may not make "
            "aspects of this analysis obsolete or cause it to break"),
        dmc.Space(h=20),
        dmc.Text("Assumptions", size="xl"),
        dmc.Text(
            "Since there is no documentation provided by Hinge, here are some assumptions I am making about the data "
            "in the export: "),
        dmc.Text("1. Unmatches, or `blocks` as Hinge refers to them, could go either direction, meaning you "
                 "could have unmatched the other person or they could have unmatched you. Hinge does not include any "
                 "additional data in these events to tell who unmatched who"),
        dmc.Text(
            "2. Matches without a like in the same event mean that someone liked you first, and you chose to match "
            "with them (i.e. they liked you first)"),
        dmc.Space(h=30)]),

    # section for uploading files
    html.Div([
        dmc.Text("Upload Files", style={"fontSize": 28}, weight=500),
        dmc.Text("Upload the `matches.json` and the `user.json` files from the zipped Hinge export for analysis."),
        dmc.Space(h=20),
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                "fontSize": 20,
                'font-family': "Open Sans, verdana, arial, sans-serif"
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload')
    ]),

    # show links to the other pages
    dmc.Text("Data Insights", style={"fontSize": 28}, weight=500),
    dmc.Text("After uploading your data files, you can click on the page links below to see insights "
             "from the data provided by Hinge."),
    dmc.Space(h=10),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name'].title()}", href=page["relative_path"],
                     style={"fontSize": 20, 'font-family': "Open Sans, verdana, arial, sans-serif"})
        ) for page in dash.page_registry.values() if page["name"] != "Home"
    ]),
    dmc.Space(h=20),

    # container element at the bottom of the page for multi-page setup
    dash.page_container,

])


def parse_uploaded_file_contents(list_of_file_contents, list_of_file_names):
    if not os.path.exists(USER_FILE_UPLOAD_DIRECTORY):
        os.makedirs(USER_FILE_UPLOAD_DIRECTORY)

    for file_content, file_name in zip(list_of_file_contents, list_of_file_names):
        uploaded_file_data = file_content.encode("utf8").split(b";base64,")[1]

        with open(os.path.join(USER_FILE_UPLOAD_DIRECTORY, file_name), "wb") as uploaded_file:
            uploaded_file.write(base64.decodebytes(uploaded_file_data))

        # return an html Div of the uploaded file names to display to the user
        return html.Div([
            html.Div(
                dmc.Text(file_name, style={"fontSize": 16, 'font-family': "Open Sans, verdana, arial, sans-serif"})
            ) for file_name in list_of_file_names
        ])


@callback(Output('output-data-upload', 'children'),
          Input('upload-data', 'contents'),
          State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_uploaded_file_contents(list_of_contents, list_of_names)]
        return children


if __name__ == '__main__':
    app.run(debug=True)