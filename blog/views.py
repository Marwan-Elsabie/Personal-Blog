from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Comment , Profile , Follow , Like , Bookmark , Notification  
from .forms import CommentForm, PostForm , ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest , JsonResponse
from django.contrib.auth.models import User


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post-detail', pk=post.pk)
    return redirect('post-detail', pk=post.pk)


@login_required
def delete_comment(request, pk):
    try:
            comment = get_object_or_404(Comment, id=pk)
            post_pk = comment.post.id
            if request.user == comment.author or request.user == comment.post.author:
                comment.delete()
                messages.success(request, 'Comment deleted successfully!')
            else:
                messages.error(request, 'You are not authorized to delete this comment!')
            return redirect('post-detail', pk=post_pk)
    except ValueError:
        return HttpResponseBadRequest("Invalid UUID format")

def profile(request, username):
    target_user = get_object_or_404(User, username=username)
    is_followed = target_user.profile.is_followed_by(request.user) if request.user.is_authenticated else False
    
    # Always load saved posts for the profile owner
    saved_posts = Post.objects.filter(
        bookmarked_by__user=target_user
    ).order_by('-bookmarked_by__created_at') if target_user == request.user else None
    
    context = {
        'target_user': target_user,
        'is_followed': is_followed,
        'follower_count': target_user.profile.follower_count(),
        'following_count': target_user.profile.following_count(),
        'followers': target_user.followers.all(),
        'saved_posts': saved_posts,
    }
    return render(request, 'blog/profile.html', context)

@login_required
def profile_update(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'blog/profile_update.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            for post in context['posts']:
                post.is_liked = post.is_liked_by_user(self.request.user)
                post.is_bookmarked = post.bookmarked_by.filter(user=self.request.user).exists()
        return context

class PostDetailView(DetailView):
    model = Post
    slug_field = 'id'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object 
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        liked = post.toggle_like(request.user)
        if liked:  # Only create notification on like (not unlike)
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='like',
                post=post
            )
        return JsonResponse({'liked': liked, 'like_count': post.like_count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def toggle_bookmark(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            bookmark.delete()
            return JsonResponse({'bookmarked': False})
        return JsonResponse({'bookmarked': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    is_liked = post.is_liked_by_user(request.user) if request.user.is_authenticated else False
    context = {
        'post': post,
        'is_liked': is_liked,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    if request.method == "POST":
        if target_user == request.user:
            return JsonResponse({'error': 'Cannot follow yourself'}, status=400)
            
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target_user)
        if not created:
            follow.delete()
        
        return JsonResponse({
            'following': created,
            'follower_count': target_user.profile.follower_count()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def logged_in_user_profile(request):
    # Redirect to the profile view to ensure consistent handling
    return redirect('profile', username=request.user.username)

@login_required
def notifications(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    # Mark notifications as read when viewed
    request.user.notifications.filter(read=False).update(read=True)
    return render(request, 'blog/notifications.html', {'notifications': notifications})

@login_required
def saved_posts(request):
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')
    posts = [bookmark.post for bookmark in bookmarks]
    return render(request, 'blog/saved_posts.html', {'posts': posts})


