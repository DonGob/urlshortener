from django.db import models
from django.utils import timezone

class DataManager(models.Manager):
    def shortcode_exists(self, shortcode):
        existing_shortcodes = self.values_list('shortcode', flat=True)
        if shortcode in existing_shortcodes:
            return True
        else:
            return False
    
class LinkMapping(models.Model):
    originalUrl = models.CharField(max_length=256)
    shortcode = models.CharField(max_length=6, primary_key = True)
    created = models.DateTimeField(auto_now_add=True)
    lastRedirect = models.DateTimeField('time of last redirection', null=True)
    redirectCount = models.IntegerField(default=0)
    objects = DataManager()

    def update_last_redirect_and_count(self):
        self.lastRedirect = timezone.now()
        self.redirectCount += 1
        self.save()


