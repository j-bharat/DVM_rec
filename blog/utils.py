from django.contrib.auth.models import User
from .models import Follow


def get_next(request):
    
    return request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))


def get_people_user_follows(user):
    
    ul = Follow.objects.filter(from_user=user).values_list('to_user', 
        flat=True)
    return User.objects.filter(id__in=ul)


def get_people_following_user(user):
    
    ul = Follow.objects.filter(to_user=user).values_list('from_user', 
        flat=True)
    return User.objects.filter(id__in=ul)


def get_mutual_followers(user):
    
    follows = Follow.objects.filter(from_user=user).values_list('to_user',
        flat=True)
    following = Follow.objects.filter(to_user=user).values_list('from_user',
        flat=True)
    return User.objects.filter(
        id__in=set(follows).intersection(set(following)))