from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django import forms

class Application(models.Model):
  id = models.AutoField(primary_key=True)

  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100, unique=True)
  created_dt = models.DateField(default=timezone.now)
  phone = models.CharField(max_length=10)
  zipcode = models.CharField(max_length=10)

  APPLICATION_STEPS = (
    (1, 'applied'),
    (2, 'quiz_started'),
    (3, 'quiz_completed'),
    (4, 'onboarding_requested'),
    (5, 'onboarding_completed'),
    (6, 'hired'),
    (7, 'rejected'))
  step = models.IntegerField(choices=APPLICATION_STEPS, default=1)

class ApplicationForm(forms.ModelForm):
  class Meta:
    model = Application
    fields = ['name', 'phone', 'zipcode']
