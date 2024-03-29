## Overview
Hinge allows users to request an export of their personal data that was collected while they were using the app. If you have a Hinge account, you can request your data by going to Settings -> Download My Data. It typically takes between 24 and 48 hours to fulfill this request, and once the data are ready, Hinge provides a `.zip` file with your personal data.

### The Data Export Provided by Hinge
The data export provided by Hinge contains several files, but the main thing is the `index.html` file, which is used to render a web page with tabs showing different data. The tabs provided by Hinge are labeled: User, Matches, Prompts, Media, Subscriptions, Fresh Starts, and Selfie Verification. Aside from viewing changes to your prompts or seeing which pictures you've uploaded, these data are not particularly useful, especially on the Matches tab which should be the most interesting part.

The Matches tab in the Hinge export contains a list of "Matches", or rather "interactions" as I call them in this project, like this:

**Match # 1**
2024-01-22 20:13:22
Like

**Match # 2**
2024-01-23 20:15:42
Like

**Match # 3**
2024-01-23 20:37:27
Match

2024-01-23 20:39:45
Chat: Hello, World!

2024-01-23 21:49:26
Remove

The list of Matches provided by Hinge leaves a lot to be desired, which is why I decided to build this project analyzing and visualizing interesting insights from the Hinge data export.

## How To Run The App
The application is a simple Dash Plotly application that runs on port `8050`. Start the application after installing project dependencies and open a browser window to localhost:8050.

The page will render with information about the app and instructions on how to use it. The page has two different tabs under the "Data Insights" section, which show match data or user data depending on which one is selected from the home page. Click on "Matches" or "Users" to show the information and graphs for either topic. The visualizations will initially show as blank graphs until a file has been upload and the "Reload Graphs" button has been clicked.

The "Upload Files" section allows users to upload a `matches.json` or `user.json` file for analysis for either tab. At the moment, the program expects the file to be called `matches.json` or `user.json`, as they are in the export provided by Hinge. After a file has been selected, it should show the uploaded file name under the upload box. From here, click the "Reload Graphs" button to reload the graphs with the uploaded data.

## Caveats
Hinge changes and updates the schema of the data export from time to time, and that may or may not break the current analysis code and make things obsolete. So far, I haven't experienced any schema changes that have broken my code, but I assume that over time, changes will occur and things will no longer work. I haven't found a way to stay up to date with their schema changes at this time.

## Assumptions
Since there is no documentation provided by Hinge, here are some assumptions I am making about the data:
1. Blocks, or unmatches (`where block_type = 'remove'`) could go either direction, meaning that block could represent someone removing the match with you, or it could represent you removing the block with someone else
	1. I assume this also includes people you come across while swiping that you want to remove from the deck
2. Matches without a like in the same event mean that someone liked you first, and you matched with them (i.e. there was no outgoing like sent first)

## Scenario Matrix
There are several possible scenarios happening in the export data in what Hinge refers to as "matches". These are not all "matches", because some events are simply outgoing likes that were not reciprocated. This is why I refer to them as **interactions**, where an interaction represents the encounters (likes, matches, chats, blocks) that occurred between you and another person. 

Here are the different scenarios of interactions that occur in the data: 

| Like | Match | Chats | Block | Meaning |
| ---- | ---- | ---- | ---- | ---- |
| X |  |  |  | You sent an outgoing, the person did not like you back |
| X | X | X |  | You sent an outgoing like, the other person liked you back, at least one message was exchanged |
|  | X | X |  | You received an incoming like, you liked the other person back and at least one message was exchanged |
|  |  |  | X | The match was removed or "unmatched", can't tell who unmatched who. For some reason, a lot of these exist without any other information and there is no way to tell which interaction it was originally linked to |
|  | X |  | X | You received an incoming like, you liked the other person back, no messages were exchanged, and the match was removed |

## What's next
I have a long list of enhancements that I want to do to the application to make it better. To see what's on deck, check out the [Projects](https://github.com/users/smpotts/projects/2) tab in the repo. 