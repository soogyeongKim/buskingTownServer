from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from buskingTownServer import settings
from rest_framework.authtoken.models import Token

#장고 기본 제공 되는 user 모델과 1대1매핑 하여 확장
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, unique=False, on_delete=models.CASCADE, blank=True)
    user_phone = models.CharField(max_length=20, blank=True)
    user_image = models.ImageField(upload_to='user_profile/', null=True, blank=True)

    def get_followings(self):
        followings = Connections.objects.filter(user=self.user)
        return followings

# post_save 시그널을 받아 user 토큰을 생성한다.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

#버스커 모델도 user모델의 확장 user에서 제공하는 기본키를 사용하지 않고 busker_id로 기본키 관리
class Busker(models.Model):
    user = models.OneToOneField(User, unique=False, on_delete=models.CASCADE)
    busker_id = models.AutoField(primary_key=True)
    busker_name = models.CharField(null=True, max_length=50, blank=True, unique=True)
    busker_type = models.IntegerField(null=True, blank=True)
    team_name = models.CharField(null=True, max_length=50, blank=True)
    busker_tag = models.CharField(null=True, max_length=200, blank=True)
    busker_phone = models.CharField(null=True, max_length=20, blank=True)
    busker_image = models.ImageField(upload_to='certification/', null=True, blank=True)
    certification = models.NullBooleanField(default=None, blank=True)
    like_counts = models.IntegerField(null=True, blank=True)
    follower_counts = models.IntegerField(null=True, blank=True)
    coin = models.IntegerField(null=True, blank=True)

    def get_followers(self):
        followers = Connections.objects.filter(following=self.busker_id)
        return followers

class Connections(models.Model):
    connection_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, unique=False, related_name="friendship_creator_set", on_delete=models.CASCADE)
    following = models.ForeignKey(Busker, unique=False, related_name="friend_set", on_delete=models.CASCADE)





