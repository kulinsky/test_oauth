from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

import json


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True)

    photo = models.CharField(max_length=100, blank=True, null=True)

    _friends = models.TextField(blank=True, null=True)
    friends = property()

    @friends.setter
    def friends(self, value):
        if not isinstance(value, list):
            raise ValueError('friends must be a list')
        self._friends = json.dumps(value)

    @friends.getter
    def friends(self):
        return json.loads(self._friends) if self._friends else None

    @property
    def full_name(self):
        return '{}{}'.format(self.last_name, self.first_name)



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)

