from django.conf.urls import include, url
from django.views.generic import TemplateView

import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    
    url(r'^main/$', 'drchrono.views.main', name='main'),

    # url(r'^search/$', 'drchrono.views.search', name='search'),

    # url(r'', 'drchrono.views.login_failed', name='loginfailed')

    url(r'^main/edit-email/$', 'drchrono.views.edit_email', name='editemail'),
    url(r'^main/send-email-default/$', 'drchrono.views.send_email_default', name='sendemaildefault'),
    url(r'main/send-email-custom/$', 'drchrono.views.send_email_custom', name='sendemailcustom'),
    url(r'^logout/$', 'drchrono.views.logout', name='logout'),
]
