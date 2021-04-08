from pprint import pprint

from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from braces import views

from .forms import GameCreateForm
from .models import Game



class GameListView(LoginRequiredMixin,ListView):
    model = Game
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GameCreateForm()
        return context


class GameDetailView(LoginRequiredMixin,DetailView):
    model = Game
    

class GameCreateView(LoginRequiredMixin, views.JSONResponseMixin, views.AjaxResponseMixin, CreateView):
    model = Game
    form_class = GameCreateForm
    
    def get_ajax(self, request, *args, **kwargs):
        pprint(request)
        context = {
            'form': self.get_form()
        }
        html_form = render_to_string('games/partials/game_create_form.html',
            context,
            request=request,
        )       
        json_dict = {
            'html_form': html_form,
        }
        return self.render_json_response(json_dict)
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save() 
        return HttpResponseRedirect(obj.get_absolute_url())