# -*- coding: utf-8 -*-
"""
Definition of urls for TechPractice2017.
"""

from datetime import datetime
from django.conf.urls import url,include
#import django.contrib.auth.views
from django.contrib import admin

import app.forms
#import app.views
from app import views as core_views
from django.contrib.auth import views as auth_views

#from django.contrib.auth import views as auth_views
#from mysite.core import views as core_views

#urlpatterns = [
#    #url(r'^$', core_views.home, name='home'),
#    url(r'^login/$', views.login, name='login'),
#    url(r'^logout/$', views.logout, name='logout'),
#    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--
#    url(r'^admin/', admin.site.urls),
#]


# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', core_views.home, name='home'),
    url(r'^about', core_views.about, name='about'),
    url(r'^order_asc', core_views.order_asc, name='order_asc'),
    url(r'^order_desc', core_views.order_desc, name='order_desc'),
    url(r'^rnd_evnt', core_views.rnd_evnt, name='rnd_evnt'),
    url(r'^creating', core_views.creating, name='creating'),
    url(r'^voting', core_views.voting, name='voting'),
    url(r'^votedate/(?P<evtdateid>[0-9]+)', core_views.votedate, name='votedate'),
    url(r'^event_date_creating', core_views.event_date_creating, name='event_date_creating'),
    url(r'^stats', core_views.stats,name='stats'),
    url(r'^evnt/(?P<id>[0-9]+)',core_views.evnt,name='evnt' ),
    url(r'^search',core_views.search, name='search'),

    url(r'^login', core_views.LoginView.as_view(), name='login'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--

    #url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout', auth_views.logout, name='logout'),
    #url(r'^about', login_required(core_views.about), name='homelogin'),


    #url(r'^admin/', admin.site.urls),

    #url(r'^login/$',
    #    django.contrib.auth.views.login,
    #    {
    #        'template_name': 'app/login.html',
    #        'authentication_form': app.forms.BootstrapAuthenticationForm,
    #        'extra_context':
    #        {
    #            'title': 'Log in',
    #            'year': datetime.now().year,
    #        }
    #    },
    #    name='login'),
    #url(r'^logout$',
    #    django.contrib.auth.views.logout,
    #    {
    #        'next_page': '/',
    #    },
    #    name='logout'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
