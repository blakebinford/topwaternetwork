from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from subnetwork.models import SubNetwork
# Create your models here.


class FishingReport(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User)
    votes_total = models.IntegerField(default=1)
    sub_network = models.ForeignKey(SubNetwork)

    def get_absolute_url(self):
        return reverse('posts:report_detail',
                       args=[self.id,
                             self.slug])

    def __str__(self):
        return '{}'.format(self.title)


class Comment(models.Model):
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    parent_report = models.ForeignKey(FishingReport)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.author, self.parent_report)
