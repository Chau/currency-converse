# -*- coding:utf-8 -*-

from django.shortcuts import render, render_to_response
from django.http import JsonResponse, HttpResponseNotAllowed

from exchangerates.conversion import ConvertRate
from exchangerates.const import CURRENCIES


def index(request):
    return render_to_response('main/index.html', locals())


def currency_converse(request):
    '''
    POST: /api/currency/converse
    :param request:
    :return:
    '''
    if request.method == 'POST':
        errors = []
        from_currency = request.POST.get('from_currency', '').strip()

        if not from_currency:
            errors.append('Param "from_currency" can\'t be empty' )
        if from_currency not in CURRENCIES:
            errors.append('Param "from_currency" must be one of "{}" values'.format(','.join(CURRENCIES)))

        to_currency = request.POST.get('to_currency', '').strip()
        if not to_currency:
            errors.append('Param "to_currency" can\'t be empty')
        if to_currency not in CURRENCIES:
            errors.append('Param "to_currency" must be one of "{}" values'.format(','.join(CURRENCIES)))

        try:
            amount = float(request.POST.get('amount'))
        except ValueError:
            errors.append('Bad type of "amount" param')

        if errors:
            return JsonResponse({'status': 400,
                                 'error': {
                                     'code': 1,
                                     'message': errors
                                 }})

        converse = ConvertRate(from_currency=from_currency, to_currency=to_currency, amount=amount)

        try:
            converted_amount = converse.convert()
        except Exception as e:
            return JsonResponse({'status': 500,
                                 'error':{
                                     'code': 2,
                                     'message': 'Internal error'
                                 }})
        return JsonResponse({'converted_amount': converted_amount, 'currency': to_currency})
    else:
        return HttpResponseNotAllowed(['POST',])

# end