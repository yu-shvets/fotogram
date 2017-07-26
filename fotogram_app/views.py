from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Posts, Comments
from django.forms import ModelForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404

# Create your views here.


class PostListView(ListView):

    model = Posts
    template_name = 'index.html'
    paginate_by = 2

    def get_queryset(self):

        queryset = super(PostListView, self).get_queryset()
        q = self.request.GET.get('query')

        if q:
            return queryset.filter(description__icontains=q.strip())
        elif self.kwargs.get('user_id'):
            return queryset.filter(user=self.kwargs['user_id'])
        else:
            return queryset

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        return context


class CommentForm(ModelForm):

    class Meta:
        model = Comments
        fields = ['author', 'comment']


class PostDetailView(DetailView):

    model = Posts
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object.pk}, hide_condition=True)
        context['comments'] = Comments.objects.filter(post=self.object.pk)
        return context


class CommentCreate(CreateView):

    model = Comments
    form_class = CommentForm
    template_name = 'index.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.post = Posts.objects.get(pk=self.kwargs['post_id'])
        obj.save()
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(CommentCreate, self).get_context_data(**kwargs)
        context['object_list'] = Posts.objects.all()
        return context

    def get_success_url(self):
            return reverse('home')


class PostForm(ModelForm):

    class Meta:
        model = Posts
        fields = ['photo', 'description']


class NewPostCreate(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'index.html'

    model = Posts
    form_class = PostForm
    template_name = 'newpost.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect('/')

    def get_context_data(self, **kwargs):
        context = super(NewPostCreate, self).get_context_data(**kwargs)
        context['object_list'] = Posts.objects.all()
        return context


def like_post(request):
    post_id = request.GET.get('post_id', None)
    like = 0
    if post_id:
        post = Posts.objects.get(id=int(post_id))
        if post is not None:
            like = post.like + 1
            post.like = like
            post.save()
    return HttpResponse(like)


def create_comment(request, post_id):

    new_comment = CommentForm(data=request.POST)
    response_data = {}

    if new_comment.is_valid():
        comment = new_comment.save(commit=False)
        comment.post = Posts.objects.get(id=post_id)
        comment.save()

        response_data['author'] = comment.author
        response_data['comment'] = comment.comment
        response_data['datetime'] = comment.datetime

    return JsonResponse(response_data)


class PostDelete(LoginRequiredMixin, DeleteView):

    model = Posts
    template_name = 'posts_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):

        obj = super(PostDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Exception('Unauthenticated user!!!')
        return obj
