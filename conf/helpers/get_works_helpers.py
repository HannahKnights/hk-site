from conf.globals import *
from .timedate_helpers import create_timestamp, is_timestamp_diff_greater_than

import os as _os
import json as _json
import math as _math

# installs
#import slugify as _slugify deprecated in python 3
import re as _re
import requests as _requests
import boto3 as _boto3


non_url_safe_char = [
    '"', '#', '$', '%', '&',
    '+', ',', '/', ':', ';',
    '=', '?', '@', '[', '\\',
    ']', '^', '`', '{', '|', '}',
    '~', "'"
]

def slugify(title):
    non_url_safe_regex = _re.compile(r'[{}]'.format(''.join(_re.escape(char) for char in non_url_safe_char)))
    if title:
        title = non_url_safe_regex.sub('', title).strip().lower()
        title = '_'.join(_re.split(r'\s+', title))
    return title


# API REQUESTS, CACHE FILE CREATION AND EXTRACTION

def call_api(page_number = None):
    """
    Using a get request query https://api.are.na/v2/channels/my-channel-name
    """
    works_json = ''
    try:
        api_url = '%s%s' % (LIST_OR_WORKS_URL, ('?page=%s' % page_number if page_number else ''))
        works_from_api = _requests.get(api_url)
        works_json = works_from_api.json()
    except:
        print('Unable to get work list from are.na')
    return works_json

def get_works_json_from_api():
    """
    Using a get request query https://api.are.na/v2/channels/my-channel-name
    """
    number_of_pages = 1
    works_json = call_api()
    total_number_of_works = works_json.get('length')
    works_per_page =  works_json.get('per')
    if total_number_of_works > works_per_page:
        # we have multiple pages, we must loop through and get additional works
        number_of_pages = _math.ceil(float(total_number_of_works) / works_per_page)
        for page_number in range(2, int(number_of_pages + 1)):
            additional_works_json = call_api(page_number = page_number)
            if additional_works_json.get('contents'):
                works_json['contents'] += additional_works_json['contents']
    return works_json

def create_title_slug(title):
    title_slug = slugify(title)
    return title_slug

def get_work_link(work):
    work_link = ''
    if isinstance(work, dict):
        work_link = '%s-%s' % (work.get('title_slug', ''), work.get('id', ''))
    return work_link

def prepare_works_for_cacheing(works_json_from_api):
    """
    Given the works json directly from the API clean it up to
    only include relevant fields, before we cache it
    """
    works = []
    works_json = works_json_from_api.get('contents', {})

    for work in works_json:
        img_urls = {}
        id = work.get('id', '')
        title = work.get('title') if work.get('title') else work.get('generated_title', '')
        title_slug = create_title_slug(title)
        content_type = work.get('class', '').lower()
        position = work.get('position','')
        content = work.get('content', '')
        content_html = work.get('content_html', '')
        description = work.get('description', '')
        description_html = work.get('description_html', '')

        if content_type == 'image':
            image_details = work.get('image')
            img_urls['medium'] = image_details.get('display', {}).get('url') or ''
            img_urls['large'] = image_details.get('large', {}).get('url') or ''
            img_urls['original'] = image_details.get('original', {}).get('url') or ''

        if id and title:
            work_info = {
                'id' : id,
                'title' : title,
                'title_slug' : title_slug,
                'position' : position,
                'content' : content,
                'content_html' : content_html,
                'content_type' : content_type,
                'description' : description,
                'description_html' : description_html,
                'imgs' : img_urls
            }
            works.append(work_info)
    return {'works' : works}

def create_works_content_for_cacheing():
    """
    Get and process the works from an API adding a
    timestamp into a 'creation_timestamp' field so
    that we know when to re-fetch this info
    """
    works_json_from_api = get_works_json_from_api()
    works_for_cacheing = prepare_works_for_cacheing(works_json_from_api)
    works_for_cacheing['creation_timestamp'] = create_timestamp()
    return works_for_cacheing

def create_s3_resource():
    """
    Create the s3 resource. This requires the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` to
    be set in env variables.
    """
    s3_resource = None
    try:
        s3_resource = _boto3.resource('s3')
    except Exceptions as error:
        print(error)
        print('Your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be stored in env variables')
        print('Set these as follows `export export AWS_ACCESS_KEY_ID="my-secret-key"`')
    return s3_resource

def get_existing_cached_data(cache_file_object):
    """
    Used in conjunction with `get_cache_file_object` where we define the bucket
    and the file that we are requesting data from
    """
    existing_cached_data = None
    try:
        existing_cached_data = cache_file_object.get()
        success = True
    except Exception as error:
        print(error)
        pass
    return existing_cached_data

def get_cache_file_object(s3_resource):
    """
    Get the cache file object from the AWS S3 bucket.
    """
    cache_file_object = None
    try:
        cache_file_object = s3_resource.Object(S3_BUCKET_NAME, CACHE_FILENAME)
    except Exception as error:
        print(error)
        pass
    return cache_file_object


def get_cache_file_content(cache_file_object, return_json = False):
    """
    The `Body` of the AWS S3 object has the file content, check and get this.
    """
    results = ''
    if cache_file_object.get('Body'):
        works_cache_file_content = cache_file_object['Body'].read()
        cache_file_object['Body'].close()
        if not return_json:
            try:
                results = _json.loads(works_cache_file_content)
            except:
                print('The was not proper json')
                results = {}
        else:
            results = works_cache_file_content

    return results

def load_or_create_works_cache(return_works = False, force = False, verbose = False):
    """
    Check the cache file for the 'list_of_works' has not expired, if it has
    or if it does not exist then create it.

    pass force = True to ignore the last cached time

    We get the cached file list from are.na API and store the file in a D3 bucket on AWS.
    """
    create_cache_file_required = True
    existing_cached_data = {}
    works_cache_content = None

    s3_resource = create_s3_resource()

    if s3_resource:

        cache_file_object = get_cache_file_object(s3_resource)

        if cache_file_object:

            existing_cached_data = get_existing_cached_data(cache_file_object)
            if verbose:
                print('works_cache_exists: %s' % existing_cached_data)

            # if cache data exists we need to check it is still valid
            if existing_cached_data and not force:

                works_cache_content = get_cache_file_content(existing_cached_data)
                if works_cache_content and works_cache_content.get('creation_timestamp'):
                    # if we have read the file then lets check the timestamp
                    timestamp_now = create_timestamp()
                    works_cache_timestamp = '%s' % works_cache_content.get('creation_timestamp')
                    timestamp_expired = is_timestamp_diff_greater_than(timestamp_now, works_cache_timestamp, minutes = CACHE_MINUTES)
                    if not timestamp_expired:
                        create_cache_file_required = False
                        works_cache_content = _json.dumps(works_cache_content)
                if verbose:
                    print('works_cache_content_has_expired: %s' % create_cache_file_required)

            if create_cache_file_required:
                works_content = create_works_content_for_cacheing()
                works_content_json = _json.dumps(works_content)
                cache_file_object.put(Body = (works_content_json)) # put the data on s3
                works_cache_content = works_content_json
                if verbose:
                    print('\ncreated and uploaded a new works cache\n')
        else:
            # no cache_file_object
            if verbose:
                print('Unable to continue, no cache_file_object available in the specified bucket')
    else:
        # no s3_resource
        if verbose:
            print('Unable to continue, no s3 resource available')

    if return_works:
        return works_cache_content


def get_works(return_json = True, force = False, verbose = False):
    works = load_or_create_works_cache(return_works = True, force = force, verbose = verbose)
    if return_json:
        try:
            works = _json.loads(works)
        except:
            works = {}
    return works

def get_work_html_list(force = False, verbose = False):
    work_html_list = []
    all_works_list = get_works(force = force, verbose = verbose).get('works') or []

    for work in all_works_list:
        type = work.get('content_type')
        if type == 'image':
            image_urls = work.get('imgs') or {}
            if image_urls.get('large'):
                alt_text = work.get('description') or ''
                img_url = image_urls.get('large') or ''
                work_html_list.append('<img class="hidden" src="%s" alt="%s">' % (img_url, alt_text))
        elif type == 'text':
            content_html = work.get('content_html') or ''
            if content_html:
                work_html_list.append('<div class="text hidden">%s</div>' % content_html)
    return work_html_list
