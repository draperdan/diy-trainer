from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(
        regex=r'^(?P<guide_version>\d+)/$',
        view=views.EmailSignUpCreateView.as_view(),
        name='email_signup'
    ),
    url(
        regex=r'^(?P<guide_version>\d+)/feedback/$',
        view=views.FeedbackCreateView.as_view(),
        name='guide_feedback'
    ),
    url(
        regex=r'^(?P<guide_version>\d+)/feedback/thanks/$',
        view=TemplateView.as_view(template_name='guides/feedback_submitted.html')
    )
)
