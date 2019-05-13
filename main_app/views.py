from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, DetailView,
                                    CreateView, UpdateView, DeleteView)
from . import models
# Create your views here.

class HomeTemplateView(TemplateView):
    template_name = 'main_app/home.html'

class SitesListView(ListView):
    context_object_name = 'sites'
    model = models.Sites

class SitesDetailView(DetailView):
    context_object_name = 'sites_detail'
    model = models.Sites
    template_name = 'main_app/sites_detail.html'

class SiteCreateView(CreateView):
    model = models.Sites
