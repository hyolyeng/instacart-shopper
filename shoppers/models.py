from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django import forms
from django.core.validators import RegexValidator

class Application(models.Model):
  id = models.AutoField(primary_key=True)

  name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100, unique=True)
  created_dt = models.DateField(default=timezone.now)
  
  phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Phone number must contain only digits, of length 9-15")
  phone = models.CharField(validators=[phone_regex], max_length=16)
  
  zip_regex = RegexValidator(regex=r'^\d{5}$', message="Zip code should be 5 digits. eg. 94085")
  zipcode = models.CharField(validators=[zip_regex], max_length=10)

  APPLICATION_STEPS = (
    (1, 'applied'),
    (2, 'quiz_started'),
    (3, 'quiz_completed'),
    (4, 'onboarding_requested'),
    (5, 'onboarding_completed'),
    (6, 'hired'),
    (7, 'rejected'))
  step = models.IntegerField(choices=APPLICATION_STEPS, default=1)

  @staticmethod
  def step_str(step):
    return [s for s in Application.APPLICATION_STEPS if s[0] == step][0][1]

class ApplicationForm(forms.ModelForm):
  class Meta:
    model = Application
    fields = ['name', 'phone', 'zipcode']
