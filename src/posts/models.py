from django.db import models
from django.core.urlresolvers import reverse

def upload_location(instance, filename):
    # Its returning a relative string where it's going.
    return "%s/%s" %(instance.id,filename)




# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True, blank=True,
    width_field="width_field",
    height_field="height_field")
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now= True, auto_now_add = False)
    timestap = models.DateTimeField(auto_now= False, auto_now_add = True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"id":self.id})
    #This makes sure that all the datas are in this order.
    class Meta:
        ordering = ["-timestap", "-updated"]
