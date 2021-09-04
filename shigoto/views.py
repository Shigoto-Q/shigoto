from django.conf import settings
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Shigoto"
        context["description"] = "The best task scheduler there is"
        context["content"] = "TBD"
        return context
