"""
    Defines global variables to be accessed throughout project
"""


CACHE_MINUTES = 5
CACHE_FILENAME = 'works.json'
ARENA_BASE_API_URL = 'https://api.are.na/v2/channels/'
ARENA_CHANNEL_SLUG = 'hk-work-images'
LIST_OR_WORKS_URL = ARENA_BASE_API_URL + ARENA_CHANNEL_SLUG
S3_BUCKET_NAME = 'hmk-site'
S3_BUCKET_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET_NAME)
