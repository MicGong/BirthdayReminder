import requests
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, JsonResponse
from django.http.request import QueryDict
from django.template import Template, Context
from django.core.mail import EmailMessage
from models import *
from forms import *

# from string import Template as str_template

# from social.apps.django_apps.default.models import *


def get_access_token(user):
    user_temp = User.objects.get(id=user.id)
    if not user_temp:
        return ''
    social = user_temp.social_auth.filter(provider = 'drchrono')

    for s in social:
        print 'social', s

    # user = UserSocialAuth.objects.get(uid = )
    # print 'social user is', social[0].user.id, 'request uid is', uid
    # social = user.social_auth.get(id=uid)
    return social[0].extra_data['access_token']

def request_paginated(url, headers):
    results = []
    while url:
        data = requests.get(url, headers=headers).json()
        results.extend(data['results'])
        url = data['next']
    return results

@login_required
def main(request):
    access_token = get_access_token(request.user)
    headers = {
        'Authorization': 'Bearer {0}'.format(access_token),
    }
    patients_url = 'https://drchrono.com/api/patients'
    patients = request_paginated(patients_url, headers)
    email = Email.objects.first()
    print email
    return render(request, 'main.html', {'patients':patients, 'email':email})

# @login_required
# def search(request):
#     print request.POST
#     form = SearchForm(request.POST)
#     if not form.is_valid():
#         print 'search form in not valid'
#         return render(request, 'main.html', {'form':form})
#     access_token = get_access_token(request.user.id)
#     patients_filter_url = 'https://drchrono.com/api/patients_summary/?'
#     if form.cleaned_data['first_name']:
#         print 'search for', first_name
#         patients_filter_url += 'first_name=' + form.cleaned_data['first_name'] + '&'
#     if form.cleaned_data['last_name']:
#         print 'search for', last_name
#         patients_filter_url += 'last_name=' + form.cleaned_data['last_name'] + '&'
#     if form.cleaned_data['date_of_birth']:
#         print 'search for', date_of_birth
#         patients_filter_url += 'date_of_birth=' + form.cleaned_data['date_of_birth'] + '&'
#     if form.cleaned_data['gender']:
#         print 'search for', gender
#         patients_filter_url += 'gender=' + form.cleaned_data['gender'] + '&'
#     patients_filter_url = patients_filter_url[:-1]
#     print 'search url', patients_filter_url
#     patients = request_paginated(patients_filter_url, \
#         headers={'Authorization': 'Bearer {0}'.format(access_token),})
#     return render(request, 'main.html', {'patients':patients, 'form':form})

@login_required
def edit_email(request):
    form = EmailForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'error':form.errors, 'title':'', 'body':''})
    email = Email.objects.first()
    title = form.cleaned_data['title'].strip()
    body = form.cleaned_data['body'].strip()
    if not email:
        email = Email(title = title, body = body)
    else:
        email.title = title
        email.body = body
    email.save()
    return JsonResponse({'title':title, 'body':body})

@login_required
def send_email_default(request):
    email_default = Email.objects.first()
    # template = Template(email_default.body)
    first_names = request.POST.getlist('first_names')
    last_names = request.POST.getlist('last_names')
    emails = request.POST.getlist('emails')
    for elem in zip(emails, first_names, last_names):
        email_content = email_default.body.replace('[first_name]', elem[1]).replace('[last_name]', elem[2])
        email_title = email_default.title.replace('[first_name]', elem[1]).replace('[last_name]', elem[2])
        email = EmailMessage(subject=email_title, body=email_content, to=[elem[0]])
        # email.send()
        try:
            email.send()
        except Exception as e:
            print 'Fail to send email'
            print e
            return JsonResponse({'error':str(e.args)})
    return JsonResponse({})

@login_required
def send_email_custom(request):
    title = request.POST.get('title')
    body = request.POST.get('body')
    first_names = request.POST.getlist('first_names')
    last_names = request.POST.getlist('last_names')
    emails = request.POST.getlist('emails')
    for elem in zip(emails, first_names, last_names):
        email_content = body.replace('[first_name]', elem[1]).replace('[last_name]', elem[2])
        email_title = title.replace('[first_name]', elem[1]).replace('[last_name]', elem[2])
        email = EmailMessage(subject=email_title, body=email_content, to=[elem[0]])
        try:
            email.send()
        except Exception as e:
            print 'Fail to send email', e
            return JsonResponse({'error':str(e.args)})
    return JsonResponse({})

@login_required
def logout(request):
    user_temp = User.objects.get(id=request.user.id)    
    print 'user is authenticated?', request.user.is_authenticated()
    django_logout(request)
    return redirect('/')




