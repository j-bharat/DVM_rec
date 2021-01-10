from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import Profile
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

       
    def get_absolute_url(self):
         return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def number_of_comments(self):
        return BlogComment.objects.filter(post_connected=self).count()
         




class BlogComment(models.Model):
    post_connected = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.author) + ', ' + self.post_connected.title[:40]


# class Follow(models.Model):
    
#     from_user = models.ForeignKey(User, related_name='following_links', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(User, related_name='follower_links', on_delete=models.CASCADE)
#     date_added = models.DateTimeField(default=timezone.now)

#     def __unicode__(self):
#         return str("%s is following %s" % (self.from_user.username, self.to_user.username))

#     def save(self, **kwargs):
        
#         if self.from_user == self.to_user:
#             raise ValueError("Cannot follow yourself.")
#         super(Post, self).save(**kwargs)
    
#     class Meta:
#         unique_together = (('to_user', 'from_user'),)

     
