from __future__ import absolute_import, unicode_literals
from celery import shared_task
from app.models import File, Meta
from django.utils import timezone

import datetime
import requests


@shared_task
def log_celery_success():
    print('CELERY is working yippea!')


@shared_task
def update_files():
    request = requests.get('https://www.anfe.ma/contents/en/projects/index.json')
    time = get_time_from_header(request.headers)
    update_files_from_json(request.json(), time)


def get_time_from_header(headers):
    print(headers)  # TODO: Insomnia doesn't send custom headers :(
    return timezone.now() - datetime.timedelta(days=1)  # let's use one day ago


def update_files_from_json(json, time):
    for file in json['files']:
        if need_to_update_file(file, time):
            if 'meta' in file:

                meta = file['meta']

                meta_db = Meta.objects.update_or_create(client=get_property_value(meta, 'client', ''),
                                                        color=get_property_value(meta, 'color', ''),
                                                        hidden=get_property_value(meta, 'hidden', False),
                                                        identification=get_property_value(meta, 'id', ''),
                                                        span=get_property_value(meta, 'span', ''),
                                                        title=get_property_value(meta, 'title', ''))

                file_db = File.objects.update_or_create(file=get_property_value(file, 'file', ''),
                                                        meta=meta_db[0],
                                                        sorting=get_property_value(file, 'sorting', 0))

                print('Success: Created (true) / updated (false) file:' + file_db.__str__())
            else:
                print('Error: No meta object found.')
        else:
            print('Nothing happened.')


def need_to_update_file(file, time):
    if 'file' not in file:
        print('Error: Attribute file not found.')
        return False
    elif not File.objects.filter(file=file['file']):  # Todo: Should be primary key?
        # create new file in any case
        return True
    else:
        # check update time
        return File.objects.get(file=file['file']).updated_at > time


def get_property_value(obj, key, default):
    return obj[key] if key in obj else default
