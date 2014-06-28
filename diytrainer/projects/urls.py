from django.conf.urls import patterns
from django.conf.urls import url

from . import views

urlpatterns = patterns('',
    url(
        regex=r'^(?P<slug>[-\w]+)/(?P<level>\d+)/$',
        view=views.DetailLevelView.as_view(),
        name='detaillevel_detail'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/(?P<level>\d+)/satisfied-feedback/$',
        view=views.FeedbackSatisfiedCreateView.as_view(),
        name='project_satisfied_feedback'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/(?P<level>\d+)/unsatisfied-feedback/$',
        view=views.FeedbackUnsatisfiedCreateView.as_view(),
        name='project_unsatisfied_feedback'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/(?P<level>\d+)/satisfied-feedback/thanks/$',
        view=views.SatisfiedFeedbackSubmittedTemplateView.as_view(),
        name='feedback_submitted'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/(?P<level>\d+)/unsatisfied-feedback/sorry/$',
        view=views.UnsatisfiedFeedbackSubmittedTemplateView.as_view(),
        name='feedback_submitted'
    ),
)
