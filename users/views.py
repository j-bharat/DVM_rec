from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile




def register(request):
    if request.method == 'POST':
        form= UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f"Cheers! Your account '{username}' has been activated. Log In to start connecting!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form} )
    
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and  p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Details updates Succesfully!')
            return redirect ('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
            'u_form' : u_form,
            'p_form' : p_form
             
        }
    return render ( request, 'users/profile.html', context)

class ProfileListView(ListView):
    model = Profile 
    template_name="users/allprofiles.html"
    context_object_name= 'users'
    
    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user).order_by('date_posted')

class ProfileDetailView(DetailView):
    model = Profile
    template_name="users/profiledetails.html"
    
    
    def get_object(self, **kwargs):
       pk= self.kwargs.get('pk')
       view_profile= Profile.objects.get(pk=pk)
       return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk= self.kwargs.get('pk')
        view_profile= Profile.objects.get(pk=pk)
        my_profile= Profile.objects.get(user= self.request.user)
        if view_profile.user in my_profile.following.all():
            follow= True 
        else:
            follow= False
        context["follow"]= follow
        return context



class FollowersListView(ListView):
    model= User
    template_name= 'users/followers.html'
    context_object_name= 'users'
    ordering= ['-date_posted']
    paginate_by = 5

class FollowingListView(ListView):
    model= User
    template_name= 'users/following.html'
    context_object_name= 'users'
    ordering= ['-date_posted']
    paginate_by = 5
