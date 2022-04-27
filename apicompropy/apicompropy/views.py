from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    """
    Подключить LoginRequiredMixin если заходить в приложение можно только зареганым.
    """
    template_name = "index.html"