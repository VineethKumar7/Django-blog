from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone

def upload_location(instance, filename):
    # Its returning a relative string where it's going.
    return "%s/%s" %(instance.id,filename)

class PostManager(models.Manager):
    # We are over riding the default all
    def active(self, *args, **kwargs):
        # super(PostManager, self) this get the orginal all()
         # it's inheriting from model.Manager
         # super(PostManager, self) is getting orginal all
         # Then we are appending stuff to it
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
    title = models.CharField(max_length = 120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True, blank=True,
    width_field="width_field",
    height_field="height_field")
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default = False)
    publish = models.DateField(auto_now = False, auto_now_add=False)
    updated = models.DateTimeField(auto_now= True, auto_now_add = False)
    timestap = models.DateTimeField(auto_now= False, auto_now_add = True)

    objects = PostManager()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"slug": self.slug})
    #This makes sure that all the datas are in this order.
    class Meta:
        ordering = ["-timestap", "-updated"]
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        #If exist then it is going to be recursive here
        new_slug = "%s-%s"%(slug, qs.first().id)
        return create_slug(instance, new_slug= new_slug)
    return slug

def pre_save_post_reciver(sender, instance, *args, **kwargs):
    #we know that this function assigns value to slug field
    #if value is not present in it then we do this
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(pre_save_post_reciver, sender=Post)
