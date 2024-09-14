"""Polls app configuration."""

from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Polls app configuration class."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
