from django.views.generic import TemplateView, DetailView, CreateView
from .models import Post
from followers.models import Follower
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from typing import Any
from django.forms import BaseModelForm
from django.shortcuts import render

class HomePage(TemplateView):
    http_method_names = ['get']
    template_name = 'feed/homepage.html'
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request

        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            following = list(Follower.objects.filter(followed_by=self.request.user).values_list('following', flat=True))

            if not following:
                posts =  Post.objects.order_by("-date").all()[0:30] 
            else:
                # print(following)
                posts =  Post.objects.order_by("-date").filter(author__in=following)[0:30]
        else:
            posts =  Post.objects.order_by("-date").all()[0:30]    

        context['posts'] = posts
        return context

    

class PostDetailPage(DetailView):
    template_name = 'feed/detail.html'
    http_method_names = ['get']
    model = Post    
    context_object_name = 'post'

class CreateNewPostPage(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "feed/create.html"
    fields = ['text']
    success_url = "/"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.request = request

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        post = Post.objects.create(
            text = request.POST.get('text'),
            author = request.user
        )

        return render(
            request,
            "includes/post.html",
            {
                "post": post,
                "show_detail_link": True
            },
            content_type="application/html"
        )