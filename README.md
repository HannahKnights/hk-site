# hk-site
HK website - a re-write of an existing simple static website - using the [are.na](https://dev.are.na/documentation/channels) API, AWS storage bucket and [bottle.py](https://bottlepy.org/docs/dev/).

## What's going on?

A `are.na` channel of image and text content is pulled in to display on the '/' home page of the one-page site. This can be accessed through the are.na API, which we fetch as a JSON feed. After a small amount of transformation to the data, this is uploaded to a corresponding AWS bucket as a JSON file. The JSON file acts as the data cache and is not recreated more than every 5 minutes.
(see `conf.helpers.get_works_helpers.py` for next to all of the logic for this)

## To run

To get the site going simply run `python base.py` - however this may well fail because it relies on the following variables being set in your environment:

- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- S3_BUCKET_NAME
