from typing import Any
from django.contrib.auth.models import User
from django.forms import BaseModelForm
from django.views.generic import DetailView, View, TemplateView, UpdateView
from feed.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from typing import Any
from followers.models import Follower
from .forms import ProfileUpdateForm
from django.urls import reverse
from django.shortcuts import redirect

# Create your views here.
class ProfileDetailPage(DetailView):
    http_method_names = ["get"]
    model = User
    template_name = 'profiles/detail.html'
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count()
        context['total_followers'] = Follower.objects.filter(following=user).count()

        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()

        return context
    
class FollowPage(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:     
        data = request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")  
        
        if data["action"] == "follow":
            #Follow
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            #UnFollow  
            try:
                follower = Follower.objects.get(followed_by = request.user, following = other_user)  
            except Follower.DoesNotExist:
                follower = None 

            if follower:
                follower.delete()       
        
        return JsonResponse({
            "success": True, 
            "wording": "Unfollow" if data['action'] == 'follow' else "Follow"
        })


class ProfileUpdatePage(LoginRequiredMixin,UpdateView):
    template_name = 'profiles/edit.html'
    http_method_names = ['get', 'post']
    model = User
    form_class = ProfileUpdateForm
    slug_field = 'username'
    slug_url_kwarg = 'username'

    
    def get_object(self, queryset=None) -> User:
        return self.request.user
    
    def get_success_url(self) -> str:
        return reverse('profiles:edit', kwargs={'username': self.request.user.username})
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.save()
        return redirect(self.get_success_url())

