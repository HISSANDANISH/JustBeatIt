from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from autoslug import AutoSlugField
from django.db.models.signals import post_save 
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Profile(models.Model):
    Instrument_choices = [
    ('Guitar', 'Guitar'),
    ('Drums', 'Drums'),
    ('Piano', 'Piano'),
    ('Violin', 'Violin'),
    ('Saxophone', 'Saxophone'),
    ('Keyboard', 'Keyboard'),
    ('Flute', 'Flute'),
    ('Tabla', 'Tabla'),
    ('None', 'None'),
    ]
    music_choices =[
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Folk', 'Folk'),
        ('Jazz', 'Jazz'),
        ('Blues', 'Blues'),
        ('None', 'None'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from = 'user')
    bio = models.CharField(max_length=255, blank=True)
    friends = models.ManyToManyField('Profile', blank=True)
    instruments = models.CharField(max_length=20, choices=Instrument_choices, default='None')
    like_music = models.CharField(max_length=20, choices=music_choices, default='None')

    def __str__(self):
        return str(self.user.first_name)

    def get_absolute_url(self):
        return "/accounts/{}".format(self.slug)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)

    def __str__(self):
	    return "From {}, to {}".format(self.from_user.username, self.to_user.username)


