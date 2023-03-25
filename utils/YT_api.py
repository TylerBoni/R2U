import httplib2
import os
import random
import sys
import time

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_SCOPE = ["https://www.googleapis.com/auth/youtube.upload","https://www.googleapis.com/auth/youtube.force-ssl"]
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
    scope=YOUTUBE_SCOPE,
    message=MISSING_CLIENT_SECRETS_MESSAGE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))


def add_comment(channel_id,comment_text,video_id=""):
  # Call the YouTube API to insert the comment
  if video_id == "":
    video_id = get_last_video_id(channel_id)

  if video_id == "" or comment_text == "" or channel_id == "":
    exit

  args = argparser.parse_args()
  youtube = get_authenticated_service(args)
  try:
    comment = youtube.commentThreads().insert(
        part='snippet',
        body={
            'snippet': {
                'channelId' : channel_id,
                'videoId': video_id,
                'topLevelComment': {
                    'snippet': {
                        'textOriginal': comment_text
                    }
                }
            }
        }
    ).execute()
    print(str(comment))

    # #pin comment - DOESN'T WORK
    # comment_id = comment['id']
    # youtube.comments().update(
    #     part='snippet',
    #     body={
    #         'id': comment_id,
    #         'snippet': {
    #             'isPinned': True
    #         }
    #     }
    # ).execute()

    print(f'Comment "{comment_text}" was successfully posted!')
  except HttpError as error:
    print(f'An error occurred: {error}')

def get_last_video_id(channel_id):
    # Set up the YouTube API client
    args = argparser.parse_args()
    youtube = get_authenticated_service(args)

    # Call the search.list method to retrieve videos uploaded to your channel, sorted by upload date
    request = youtube.search().list(
        part='id',
        channelId=channel_id,
        order='date',
        type='video',
        maxResults=1
    )
    response = request.execute()

    # Extract the video ID from the search results
    video_id = response['items'][0]['id']['videoId']

    # Print the video ID
    print(f"Last video ID: {video_id}")
    return video_id
