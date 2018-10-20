# -*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponseNotAllowed
# from django.views.decorators.csrf import csrf_protect



# Create your views here.

def index(request):
    return render_to_response('main/index.html', locals())


# @csrf_protect
def currency_converse(request):
    '''
    POST: /api/currency/converse
    :param request:
    :return:
    '''
    if request.method == 'POST':
        return JsonResponse({'amount': 1234, 'currency': 'dl'})
    else:
        return HttpResponseNotAllowed(['POST',])


# end