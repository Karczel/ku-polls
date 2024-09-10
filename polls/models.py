import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question model."""
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    end_date = models.DateTimeField('end date', null=True, blank=True)

    def __str__(self):
        """Return the string representation of Question class."""
        return self.question_text

    def was_published_recently(self):
        """Return the bool value of whether the poll was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return the bool value of whether the poll has been published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return the bool value of whether the poll is open for voting."""
        now = timezone.now()
        if self.end_date is None:
            return self.is_published()
        return self.pub_date <= now <= self.end_date


class Choice(models.Model):
    """Choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Return the string representation pf Choice class."""
        return self.choice_text

    @property
    def votes(self):
        """Return the number of votes for this choice"""
        return Vote.objects.filter(choice=self).count()

class Vote(models.Model):
    """Vote model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        """Return the string representation of Vote class."""
        return f"User: {self.user.username}, Choice: {self.choice.choice_text}"
