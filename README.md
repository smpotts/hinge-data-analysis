# Hinge Data Analysis
Hinge allows users to request an export of their data that was collected while they were using the app. It takes a few days to fulfill this request, and once the data are ready Hinge emails you a .zip file.

The .zip file contains several .json files pertaining to different data Hinge has collected, as well as an HTML file to render the .json data in tabs locally.

For the purposes of this analysis, I am only concerned with the data in the matches.json file.

## Analyzing Match Data
The data in the matches.json file are very difficult to work with, which no doubt is by design. After normalizing the data, they are a bit easier to work with, but the schema Hinge provides leaves a lot to be desired. Hinge does not provide an explanation of the match data in the export they give you, nor have I been able to find anything like that online. In light of that, this is my best effort to make sense of the data provided.

## Assumptions
Since the data are messy and Hinge does not provide a schema or an explanation about the data, I have made some assumptions that I will use throughout the analysis.
1. When there is an independent "like" record, it means there was an incoming like (i.e. someone liked you) 
   1. The reason I think this is the case is that users get up to 10 outgoing matches per day, so given that, one would expect to see TONS of likes (roughly 10 per day) if the data were capturing outgoing likes
2. For records that have a "match" but do not contain a "like" in the same record, this assumes that there was an outgoing like first (i.e. you liked the other person first and they matched back)
   1. This is because I believe the "like" data being captured in this data set pertain to likes a user receives not sends
3. Unmatches (blocks `where block_type = 'remove'`) could go either direction
   1. There is no indication who removed the match with who and there's no way to tell 
   2. Also includes people you come across while swiping that you want to permanently remove from the deck

### Scenario Matrix
After analyzing the data in matches.json, I have come up with my best guess of the different scenarios that are happening in the data.

| Like | Match | Chats | Block | Action/ Notes | Var Name |
| ---- | ---- | ---- | ---- | ---- | ---- |
| X |  |  |  | Received an incoming like | incoming_likes |
| X | X | X |  | Received an incoming like, sent an outgoing like back, exchanged messages | incoming_like_match_chat |
|  | X |  |  | An outgoing like was sent first, other person liked back, no messages exchanged  | outgoing_like_match |
|  |  |  | X | Unmatched, can't tell who unmatched who, no way to tell which interaction it is linked to | stray_unmatches |
|  | X |  | X | Outgoing like first, matched, no chat and unmatched | outgoing_like_match_unmatch |
|  | X | X | X | Outgoing like first, matched, chatted, unmatched | outgoing_like_match_chat_unmatch |

## Holes in the data
- There are stray blocks `where block_type = 'remove'` that cannot be tied to a like, match, chat, etc. which doesn't make sense because in order for there to be an un-match, there has to have been a like and a match
- In some cases you can't see who took what action
    - It's unclear who un-matches who
    - When we have just a match, it's not clear who liked who first
    - It's not clear whether the likes on their own can be linked to messages and chats or if they were unrequited likes
- We can have matches without a corresponding "like", which isn't possible because there has to be an outgoing like for there to have been a match

## How Hinge obfuscates data in the export
- There are no ids on the records to link the data
- The data are not in chronological order
- They only provide timestamps for the events and no other information about the exchange
- The data structure is extremely difficult to work with
- Can't tell who is doing which actions (i.e. who likes first, who unmatches who, etc.)