from django.views import generic
from django.shortcuts import render
from projects.models import Category

def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories':categories})

class ProjectsPage(generic.TemplateView):
    template_name = "projects.html"


class AboutPage(generic.TemplateView):
    template_name = "about.html"

class TestsPage(generic.TemplateView):
    template_name = "tests.html"
