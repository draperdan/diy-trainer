from django.views.generic import CreateView

from .models import GuideFeedback
from .forms import GuideFeedbackForm


class GuideFeedbackCreateView(CreateView):
    model = GuideFeedback
    form_class = GuideFeedbackForm
    success_url = 'thanks/'
