from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Auto, Make


class MainView(LoginRequiredMixin, ListView):
    def get(self, request):
        mc = Make.objects.all().count()
        al = Auto.objects.all()

        context = {'make_count': mc,
                  'auto_list': al,}
        return render(request, 'autos/auto_list.html', context)


# value in the constructor attributes
class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class MakeView(LoginRequiredMixin, ListView):
    model = Make
    # def get(self, request):
    #     ml = Make.objects.all()
    #     context = {'make_list': ml}
    #     return render(request, 'autos/make_list.html', context)


class MakeCreate(LoginRequiredMixin, CreateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')



class MakeUpdate(LoginRequiredMixin, UpdateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class MakeDelete(LoginRequiredMixin, DeleteView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


