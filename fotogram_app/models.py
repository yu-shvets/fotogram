from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Posts(models.Model):

    class Meta(object):
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-datetime']

    datetime = models.DateTimeField(auto_now_add=True)

    photo = models.ImageField(
        verbose_name="Photo",
        upload_to='photos/'
    )

    description = models.CharField(
        max_length=256,
        blank=True,
        verbose_name="Description",
        null=True
    )

    like = models.IntegerField(
        blank=True,
        verbose_name='Like',
        default=0
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}".format(self.description)


class Comments(models.Model):

    class Meta(object):
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-datetime']

    datetime = models.DateTimeField(auto_now_add=True)

    author = models.CharField(
        max_length=256,
        verbose_name="Author"
    )

    comment = models.TextField(verbose_name="Comment", blank=True, null=True)

    post = models.ForeignKey(Posts)

    def __str__(self):
        return "{}".format(self.comment)


class UserProfile(models.Model):

    user = models.OneToOneField(User, related_name='profile')
    birthday = models.DateField()
    country = models.CharField(max_length=256)
    city = models.CharField(max_length=256)

    def __str__(self):
        return "{}".format(self.user)


