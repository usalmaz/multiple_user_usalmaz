from PIL import Image
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.core.mail import send_mail

class User(AbstractUser):
    first_name = models.CharField(verbose_name="First name", max_length=255)
    last_name = models.CharField(verbose_name="Last name", max_length=255)
    country = models.CharField(verbose_name="Country name", max_length=255)
    city = models.CharField(verbose_name="City name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username

#signal used for is_active=False to is_active=True
@receiver(pre_save, sender=User, dispatch_uid='active')
def active(sender, instance, **kwargs):
    try:
        if instance.is_active and User.objects.filter(pk=instance.pk, is_active=False).exists():
            subject = 'Your account is activated'
            mesagge = '%s your account is now active. Click the link to log in your accout https://emeupci.com/accounts/login/' %(instance.first_name)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, mesagge, from_email, [instance.email], fail_silently=False)
    except:
        print("Something went wrong, please try again.")
#signal to send an email to the admin when a user creates a new account
@receiver(post_save, sender=User, dispatch_uid='register')
def register(sender, instance, **kwargs):
    try:
        if kwargs.get('created', False):
            subject = "Verificatión of the %s 's account" %(instance.username)
            mesagge = '%s, %s just registered in www.emeupci.com. Click the link to activate him https://emeupci.com/admin/. ' %(instance.first_name, instance.last_name)
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject, mesagge, from_email, [from_email], fail_silently=False)
    except:
        print("Something went wrong, please try again.")

class Country(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    access_challenge = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    website = models.URLField(max_length=255, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.city

    def get_absolute_url(self):
        return reverse('users:blog')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 250 or img.width > 250:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.image.path)



def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
