import logging, json, zlib

from google.appengine.api import taskqueue

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import models, gcs, mfl

store = gcs.Session(settings.appspot_id)

def mainpage(request):
    return render(request, 'main.html', {})

@csrf_exempt
def data_put(request):

    if request.method != 'POST':
        return render(request, 'api.html', {})

    r = models.Request()
    r.put()

    data_id = r.key().id()

    # save data to file into gcs, because it size can exceed taskqueue payload capacity (~ 100 Kb)
    store.put("%s" % data_id, zlib.compress(request.POST.get('data', '')))
    taskqueue.add(url=reverse('api_do', None, [], {}), method="POST", params={'key': data_id})
    return redirect(reverse('api_get', None, [], {'questid': data_id, }))

@csrf_exempt
def data_do(request):

    if request.method != 'POST':
        return HttpResponse('OK')

    data_id = int(request.POST.get('key', ''))
    r = models.Request.get_by_id(data_id)

    if r is None:
        logging.warning("task id not exist: %s" % data_id)
        return HttpResponse('OK')

    data = store.get("%s" % data_id)
    if data:
        data = zlib.decompress(data)

    ###########################
    # emulate longtime analyze
    ###########################
    #import time
    #time.sleep(10)
    ###########################

    answer = {"zoomDataFormat": 1}

    try:
        data = json.loads(request.POST.get('data', ''))
        answer["result"] = mfl.analyze(data)
        answer["status"] = "ok"
        r.status = 1

    except Exception, e:
        answer["status"] = "error"
        answer["error"] = "%s" % e
        r.status = 2

    r.data = json.dumps(answer)
    r.put()
    return HttpResponse('done')

def data_get(request, questid):
    data_id = 0
    try:
        data_id = int(questid)
    except:
        raise Http404()

    r = models.Request.get_by_id(data_id)
    if r is None:
        raise Http404()

    if r.status == 0: 
        return HttpResponse('inprogress')

    return HttpResponse(r.data, content_type="application/json")
