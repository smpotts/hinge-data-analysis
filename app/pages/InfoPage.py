from dash import html
import dash_mantine_components as dmc

layout = html.Div([
    dmc.Text("Info", align="center", style={"fontSize": 28}, weight=500),
    dmc.Text("This section offers a comprehensive overview of how the project works, what data is available to the user, and how to navigate the app for the best experience."),
    dmc.Space(h=20),
    dmc.Space(h=10),
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
    dmc.Space(h=30)
])