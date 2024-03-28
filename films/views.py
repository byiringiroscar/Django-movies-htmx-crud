from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model
from films.models import Film
from django.views.generic import ListView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

from films.forms import RegisterForm

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)
    

def check_username(request):
    username  = request.POST.get('username')
    if username:
        if get_user_model().objects.filter(username=username).exists():
            return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
        else:
            return HttpResponse("<div id='username-success' class='success'>This username is available</div>")
    else:
        return HttpResponse("<div id='username-error' class='error'>Username is required</div>")
    



class FilmList(ListView):
    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        user = self.request.user
        return user.films.all()
    
@login_required
def add_film(request):
    name = request.POST.get('filmname')
    if name == '':
        return render(request, 'partials/film-list.html', {'films': request.user.films.all()})
    film = Film.objects.get_or_create(name=name)[0]

    # add the film to the user's list
    request.user.films.add(film)

    # return the template with all of the users's films
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
@require_http_methods(['DELETE'])
def delete_film(request, pk):
    film = Film.objects.get(pk=pk)
    request.user.films.remove(film)
    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})



def search_film(request):
    search_text = request.POST.get('search')
    results = Film.objects.filter(name__icontains=search_text)
    context = {
        'results': results
    }
    return render(request, 'partials/search-results.html', context)