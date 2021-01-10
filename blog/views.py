from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Post, BlogComment #Follow
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import NewCommentForm



def home(request):
    context ={
        'posts' : Post.objects.all()
    
        }
    return render( request, 'blog/home.html', context)

def feed(request):
    profile= Profile.objects.get(user=request.user)
    users= [user for user in user.following.all]
    return render( request, 'blog/feed.html', {'title': 'Feed'})

class PostListView(ListView):
    model= Post
    template_name= 'blog/home.html'
    context_object_name= 'posts'
    ordering= ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):  # This is where we'll edit to go the the user's profile, and create the follower-following scheme
    model = Post
    template_name= 'blog/user_posts.html'
    context_object_name= 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        



class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = BlogComment.objects.filter(
            post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data
    
    def post(self, request, *args, **kwargs):
        new_comment = BlogComment(content=request.POST.get('content'),
                                  author=self.request.user,
                                  post_connected=self.get_object())
        new_comment.save()
        return self.get(self, request, *args, **kwargs)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields= ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
   
   

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields= ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
   
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url= '/'
        
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False







