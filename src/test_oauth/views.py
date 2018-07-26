from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "base.html"
