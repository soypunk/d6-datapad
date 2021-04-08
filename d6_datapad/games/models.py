from slugify import slugify

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from model_utils.models import TimeStampedModel



class Attribute(models.Model):
    label = models.CharField(
        _('label'),
        max_length=255,
        help_text = _("The name of your attribute.")
    )
    min_value = models.PositiveIntegerField(default=1)
    max_value = models.PositiveIntegerField(default=5)
    upgrade_multiplier = models.PositiveIntegerField(default=5)
    notes = models.TextField(
        max_length=500,
        blank=True  
    )
    

class Skill(models.Model):
    label = models.CharField(
        _('label'),
        max_length=255,
        help_text = _("The name of your skill.")
    )
    parent_attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text = _("The attribute this skill inherits a starting value form. Leave blank to have it as a standalone skill.")        
    )
    min_value = models.PositiveIntegerField(default=1)
    max_value = models.PositiveIntegerField(default=14)
    notes = models.TextField(
        max_length=500,
        blank=True
    )
    can_be_expert_skill = models.BooleanField(
        default=False,
        help_text = _("Lil6 allows for a concept of \"Expert Skills\" but not all Open D6 games use this. In addition some Lil6 Skills cannot be taken as an Expert Skill.")
    )
    
class DerivedValues(models.Model):
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        blank=True,
        null=True       
    )
    modifier = models.PositiveIntegerField(default=0)
    

class Game(TimeStampedModel):
    """
    General container for game specific data
    """
    name = models.CharField(
        _('name'),
        max_length=255,
        help_text = _("How you refer to your game.")
    )
    slug = models.SlugField(
        max_length=255,
        unique=True
    )        
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='games'
    )
    
    attributes = models.ManyToManyField(
        Attribute,
        through='GameAttributes',
        through_fields=('game', 'attribute'),
    )
    
    skills = models.ManyToManyField(
        Skill,
        through='GameSkills',
        through_fields=('game', 'skill'),
    )
    
    derived_values = models.ManyToManyField(
        DerivedValues,
        through='GameDerivedValues',
        through_fields=('game', 'derived_value')        
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
        

class GameAttributes(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)


class GameSkills(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    
class GameDerivedValues(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    derived_value = models.ForeignKey(DerivedValues, on_delete=models.CASCADE)