from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.core import serializers
from app.tasks import log_celery_success, update_files
from django.views.decorators.csrf import csrf_exempt
from .models import File

import json


def index(request):
    return HttpResponse("This is the Index page.")


def files(request):
    return JsonResponse(list(File.objects.all().values()), safe=False)


def last_file(request):
    return JsonResponse(json.loads(serializers.serialize('json', [File.objects.latest('updated_at')])), safe=False)


def last_updated_at(request):
    return JsonResponse(File.objects.latest('updated_at').updated_at, safe=False)


@csrf_exempt
def perform_update(request):
    log_celery_success()
    if request.method == 'GET':
        return HttpResponseNotAllowed(['POST'])
    elif request.method == 'POST':
        update_files()
        return HttpResponse(status=204)
    else:
        return HttpResponseForbidden
