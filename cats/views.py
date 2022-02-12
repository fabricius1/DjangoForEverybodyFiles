from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cat, Breed


class MainView(LoginRequiredMixin, ListView):
    def get(self, request):
        bc = Breed.objects.all().count()
        cl = Cat.objects.all()

        context = {'breed_count': bc,
                  'cat_list': cl,}
        return render(request, 'cats/cat_list.html', context)


# value in the constructor attributes
class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class BreedView(LoginRequiredMixin, ListView):
    model = Breed


class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')


class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    fields = '__all__'
    success_url = reverse_lazy('cats:all')

