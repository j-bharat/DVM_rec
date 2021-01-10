from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following= models.ManyToManyField(User, related_name='following', blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    # def profiles_posts(self):
    #     return self.post_set.all()
    
    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height >500 or img.width> 500:
            output_size = (500,500)
            img.thumbnail(output_size)
            img.save(self.image.path)
     
    class Meta:
        ordering = ('-date_posted',)


    



#Create your models here.
