import os, traceback
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext

from datetime import datetime
from apps.common.models import Products, Profile, Article, Newsletter, Prompt, CustomDevelopment, ProjectTypeChoices, BudgetRangeChoices
from django.contrib import messages

# Create your views here.

# LOGGER & Events
from inspect import currentframe
from helpers.logger import *
from helpers.events import *

def index(request):

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  products = Products.objects.all().order_by('-updated_at')[:3]
  blogs = Article.objects.all().order_by('-created_at')[:3]
  
  context = {
    'segment'        : 'home',
    'page_title'     : 'App Generator, Dynamic Services, Dev & Deployment Tools',
    'page_info'      : 'Modern tools for developers and Companies, Generated Digital Products (Dashboards, eCommerce, Websites)',
    'page_keywords'  : 'app generator, dashboards, web apps, generated products, custom development, ai tools, dev tools, tools for developers and companies',
    'page_canonical' : '',
    'products'       : products ,
    'articles'       : blogs
  }

  return render(request, 'pages/home2.html', context)


def show_dashboard(request):
  products = Products.objects.all()
  products_list = list(products.values())
  return JsonResponse({'products': products_list})

def custom_development(request):

  if not request.user.is_authenticated:
    messages.error(request, "You're not authenticated. Please Sign IN")

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  if request.method == 'POST':
    form_data = {}
    for attribute, value in request.POST.items():
      if attribute == 'csrfmiddlewaretoken':
        continue

      form_data[attribute] = value
    
    CustomDevelopment.objects.create(**form_data)

    return redirect(request.META.get('HTTP_REFERER'))

  context = {
    'segment'        : 'custom_development',
    'page_title'     : 'Custom Development - Need help Coding an MVP or a Complete Solution? ',
    'page_info'      : 'Get Custom Development Services from a team of experts.',
    'page_keywords'  : 'custom development, custom tools, custom generators, app generator, dashboards, web apps, generated products',
    'page_canonical' : 'custom-development/',
    'project_types'  : ProjectTypeChoices.choices,
    'budget_range'   : BudgetRangeChoices.choices
  }

  return render(request, 'pages/custom-development.html', context)

def terms(request):

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  context = {
    'segment'        : 'terms',
    'page_title'     : 'Terms - Learn how to use the App-Generator Service',
    'page_info'      : 'AppSee/App-generator Terms of Use',
    'page_keywords'  : 'terms, service terms, AppSeed terms, App-Generator Terms',
    'page_canonical' : 'terms/',
  }

  return render(request, 'pages/terms.html', context)

def about(request):

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  context = {
    'segment'        : 'about',
    'page_title'     : 'About US - Learn more about the team and the mission ',
    'page_info'      : 'More inputs regarding AppSee/App-generator service',
    'page_keywords'  : 'about, about AppSeed, about App-Generator',
    'page_canonical' : 'about/',
  }

  return render(request, 'pages/about.html', context)

def user_profile(request, username):
  profile = get_object_or_404(Profile, user__username=username)
  context = {
    'profile': profile
  }
  return render(request, 'pages/profile.html', context)

def support(request):

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  context = {
    'segment'        : 'support',
    'page_title'     : 'Premium Support via email (support@appseed.us) and Discord',
    'page_info'      : 'Get Support for Dashboards, eCommerce, Presentation Websites',
    'page_keywords'  : 'support, email support, Discord support, Tickets, app generator, dashboards, web apps, generated products, custom development',
    'page_canonical' : 'support/',
  }

  return render(request, 'pages/support.html', context)


def newsletter(request):
  if request.user.is_authenticated:
    if request.method == 'POST':
      email = request.POST.get('email')
      if not Newsletter.objects.filter(email=email).exists():
        Newsletter.objects.create(email=email)
        messages.success(request, 'Email subscribed!')
      else:
        messages.error(request, 'Email is already subscribed!')
    
    return redirect(request.META.get('HTTP_REFERER'))
  else:
    return redirect('/users/signin/')


def create_prompt(request):
  
  if request.user.is_authenticated:
    user_id = request.user.pk
  else:
    user_id = -1
  
  if request.method == 'POST':
    question = request.POST.get('question')
    Prompt.objects.create(question=question, user_id=user_id)

    return JsonResponse({'reply': 'Hello'})

  return redirect(request.META.get('HTTP_REFERER'))


# page_not_found
def handler404(request, *args, **argv):
                                   
  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  try: 

    if 'exception' in argv:
      event_404(request, str( argv['exception'] ) )
    else:
      event_404(request, str( argv ) )

  except Exception as e:
    pass

  context = {
    'page_title': 'Error 404 - Page not foumd',
  }

  return render(request, 'pages/error-404.html', context, status=404)

# server_error 
def handler500(request, *args, **argv):

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  try: 
    
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_value:
      error_message = f"{str(exc_value)}"
      stack_trace = traceback.format_exc()
      event_500(request, error_message + "\n" + stack_trace)

  except Exception as e:
    pass
  
  context = {
    'page_title': 'Error 500 - Server Error',
  }

  return render(request, 'pages/error-500.html', context, status=500)

# bad_request
def handler400(request, *args, **argv):

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )

  print (' > args:' + str(args) )
  print (' > argv:' + str(argv) )

  context = {
    'page_title': 'Error 400 - Bad Request',
  }

  return render(request, 'pages/error-400.html', context, status=400)

# permission_denied
def handler403(request, *args, **argv):

  # Logger
  func_name  = sys._getframe().f_code.co_name 
  logger( f'[{__name__}->{func_name}(), L:{currentframe().f_lineno}] ' + 'Begin' )
  
  print (' > args:' + str(args) )
  print (' > argv:' + str(argv) )

  context = {
    'page_title': 'Error 404 - Permission Denied',
  }

  return render(request, 'pages/error-403.html', context, status=403)
