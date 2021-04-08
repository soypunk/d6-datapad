from slugify import slugify

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel



class Game(TimeStampedModel):
    """
    General container for game specific settings
    """
    name = models.CharField(
        _('name'),
        max_length=255,
        help_text = _("")
        )
    slug = models.SlugField(
        max_length=255,
        unique=True)
        
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='games'
    )
        
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'slug': self.slug })