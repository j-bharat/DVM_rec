import openpyxl
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from blog.models import Post, BlogComment
from users.models import Profile
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
    #post.author.profile
    posts = Post.objects.all()
    
    user = request.user
    following = user.profile.follow.all()
    # feed = []
   
    # for profile in following:
    #     for post in profile.user.Post.objects.all():
    #         feed.append(post)

    context = {'posts' : posts, 'prifles': following}
    return render( request, 'blog/feed.html', context)

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

def export_profiles(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profile_data.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Profile Data'

    profiles = Profile.objects.all()
    rows = [
        ['Username', 'E-mail', 'Following']
    ]
    for profile in profiles:
        follow_profiles = profile.follow.all()
        follower = []
        for profile in follow_profiles:
            follower.append(profile.user.username)
        follower_str = ','.join(follower)

        row = [profile.user.username, profile.user.email, follower_str]
        row_data.append(row)

    for row in rows:
        worksheet.append(row)

    workbook.save(response)
    return response
    







