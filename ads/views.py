from .models import Ad, Fav
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.mixins import LoginRequiredMixin
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from .forms import CommentForm
from .models import Comment
from django.views import View
from django.db.models import Q

# to favorite Views
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


class AdListView(OwnerListView):
    model = Ad
    template_name = "ads/ad_list.html"

    def get(self, request):
        
        # filter funcionality
        strval =  request.GET.get("search", False)
        if strval :
            query = Q(title__icontains=strval) 
            query.add(Q(text__icontains=strval), Q.OR)
            ad_list = Ad.objects.filter(query).select_related().order_by('-updated_at')[:10]
        else :
            ad_list = Ad.objects.all().order_by('-updated_at')[:10]

        # Augment the ad_list
        for obj in ad_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        
        
        # favorites funcionality
        
        # ad_list = Ad.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]
        # ctx = {'ad_list' : ad_list, 'favorites': favorites}
        
        ctx = {'ad_list' : ad_list,
               'search': strval,
               'favorites': favorites}
        return render(request, self.template_name, ctx)


        
        # return render(request, self.template_name, ctx)




class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    
    def get(self, request, pk) :
        ad = Ad.objects.get(id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'ad' : ad, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)


class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'price', 'text', 'picture']


class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text', 'picture']


class AdDeleteView(OwnerDeleteView):
    model = Ad


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'],
                          owner=request.user,
                          ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail',
                                args=[pk]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "ads/ad_comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail',
                       args=[ad.id])


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=ad)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()


@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        ad = get_object_or_404(Ad, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, ad=ad).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
