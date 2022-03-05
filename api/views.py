from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import BBObject, BBBatch


@csrf_exempt
def upload(request):
    if request.method != 'POST':
        return JsonResponse({"error": "invalid request"})

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    try:
        BBBatch.process(body)
        return JsonResponse({
            "status": "success",
            "message": "batch %s added" % body["batch_id"]
        }, status="200")
    except BBBatch.AlreadyProcessed:
        return JsonResponse({
            "status": "fail",
            "message": "batch already processed"
        }, status="400")
    except BBBatch.InvalidSchema:
        return JsonResponse({
            "status": "fail",
            "message": "invalid schema"
        }, status="400")


def list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 100))
    first = (page - 1) * size
    last = page * size
    count = BBObject.objects.count()
    
    # TODO: these can be used for filtering
    flt_id = request.GET.get('object_id')
    flt_key = request.GET.get('key')
    flt_val = request.GET.get('val')
    #   which would make it possible to do something like:
    # objs = BBObject.objects.filter(property__key=flt_key)
    #   or:
    # objs = BBObject.objects.filter(property__value=flt_val)
    #   if such filtering criteria were provided

    objs = BBObject.objects.all()[first:last]
    return JsonResponse({
        "status": "success",
        "page": page,
        "size": size,
        "count": count,
        "data": [o.to_json() for o in objs],
    })


def retrieve(request, id):
    obj = BBObject.objects.get(object_id=id)
    return JsonResponse({
        "status": "success",
        "data": obj.to_json(),
    })


def keys(request):
    items = BBObject.objects.values_list('object_id', flat=True)
    return JsonResponse({
        "status": "success",
        "data": [key for key in items]
    })