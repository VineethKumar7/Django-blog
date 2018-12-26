from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 120)
    content = models.TextField()
    # Auto now means that evey single time it is saved in database.
    updated = models.DateTimeField(auto_now= True, auto_now_add = False)
    # auto_now_add just updates only when we add items into this field.
    timestap = models.DateTimeField(auto_now= False, auto_now_add = True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"id":self.id})
