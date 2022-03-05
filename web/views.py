from django.shortcuts import render
import json

from api.models import BBObject, BBBatch


def list(request):
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 100))
    first = (page - 1) * size
    last = page * size
    count = BBObject.objects.count()
    objs = BBObject.objects.all()[first:last]
    prev = page - 1 if page > 1 else None
    next = page + 1 if count / size > page else None

    context = {
        "page": page,
        "size": size,
        "count": count,
        "prev": prev,
        "next": next,
        "objects": [{"id": o.object_id, "props": [{"key": p.key, "value": p.value} for p in o.properties.all()]} for o in objs]
    }
    return render(request, 'web/list.html', context)


def retrieve(request, id):
    context = BBObject.objects.get(object_id=id).to_json()
    return render(request, 'web/retrieve.html', context)


def upload(request):
    message = ""
    if request.method == 'POST':

        body_json = request.POST.get("json")
        if not body_json:
            render(request, 'web/upload.html', {})

        body = json.loads(body_json)
        try:
            b = BBBatch.process(body)
            message = "SUCCESS: batch %s added" % b.batch_id
        except BBBatch.AlreadyProcessed:
            message = "ERROR: batch already processed"
        except BBBatch.InvalidSchema:
            message = "ERROR: invalid format"

    return render(request, 'web/upload.html', {"message": message})


def keys(request):
    items = BBObject.objects.values_list('object_id', flat=True)
    context = {
        "keys": ', '.join([key for key in items])
    }
    return render(request, 'web/keys.html', context)