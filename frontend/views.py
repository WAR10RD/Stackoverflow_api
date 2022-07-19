from asyncore import read
from cmath import pi
from email import message
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.core.cache import cache
import requests
from django.contrib import messages
# Create your views here.
"""
Home View
"""
class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = {}

        return context

    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            r = None
            cache_is_true = False
            cache_response = {}
            no_of_call_per_day = 0
            no_of_call_per_minute = 0
            if request.session.get('no_of_call_per_day'):
                no_of_call_per_day = request.session.get('no_of_call_per_day')
            
            if cache.get('no_of_call_per_minute'):
                no_of_call_per_minute = cache.get('no_of_call_per_minute')
                
            cache_key = request.POST.get('page')+request.POST.get('pagesize')+request.POST.get('fromdate')+request.POST.get('todate')+request.POST.get('min')+request.POST.get('max')+request.POST.get('order')+request.POST.get('sort')+request.POST.get('tagged')
            if no_of_call_per_day < 100 and no_of_call_per_minute < 5:
                if cache.get(cache_key):
                    cache_response = cache.get(cache_key)
                    cache_is_true = True
                    request.session['no_of_call_per_day'] = no_of_call_per_day + 1
                    cache.set('no_of_call_per_minute', no_of_call_per_minute+1, 60)
                else:
                    
                    r = requests.get('https://api.stackexchange.com/2.3/questions?&site=stackoverflow&', params=request.POST)
                    request.session['no_of_call_per_day'] = no_of_call_per_day + 1
                    cache.set('no_of_call_per_minute', no_of_call_per_minute+1, 60)
            else:
                
                messages.error(request, 'You exceed no of calls')

            context = super(Index, self).get_context_data(*args, **kwargs)
            try:
                if r.status_code == 200:
                    response_dict = json.loads(r.content)
                    context['data'] = response_dict['items']
                    context['page'] = response_dict['has_more']
                    context['post_info'] = request.POST

                    cache.set(cache_key, response_dict, 30*60)
                    messages.success(request, 'data from api')
            except:
                pass
            if cache_is_true:

                context['data'] = cache_response['items']
                context['page'] = cache_response['has_more']
                context['post_info'] = request.POST
                messages.success(request, 'data from cache')
            return render(request, self.template_name, context=context)

        else:

            return HttpResponse('No question was found with this params')
