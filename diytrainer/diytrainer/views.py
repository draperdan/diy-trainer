from django.views.generic import TemplateView


class RobotsView(TemplateView):
    template_name = "robots.txt"

    def render_to_response(self, context, **kwargs):
        return super(RobotsView, self).render_to_response(context, content_type='text/plain', **kwargs)
