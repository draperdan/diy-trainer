from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(
        regex=r'^(?P<project_slug>[-\w]+)/(?P<level>\d+)/$',
        view=views.DetailLevelView.as_view(),
        name='detaillevel_detail'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/satisfied/feedback/$',
        view=views.SatisfiedFeedbackCreateView.as_view(),
        name='project_satisfied_feedback'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/need-more-info/feedback/$',
        view=views.NeedMoreInfoFeedbackCreateView.as_view(),
        name='project_needmoreinfo_feedback'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/feedback/thanks/$',
        view=TemplateView.as_view(template_name="projects/feedback_submitted.html"),
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/feedback/sorry/$',
        view=TemplateView.as_view(template_name="projects/feedback_submitted_more.html"),
    )
)
