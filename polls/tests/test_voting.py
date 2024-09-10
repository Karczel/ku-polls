import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages

from .models import Question

# verify a message was set
# response = client.post(url, post_data)
# request = response.request
#
# storage = messages.get_messages(request)
# for message in storage:
#     print(message.message)
#     print(message.tags)
#     print(message.level)

class QuestionModelTests(TestCase):

    def test_can_vote_within_pub_and_end_date(self):
        """
        can_vote() returns True for questions whose pub_date
        is in the past
        and end_date
        is in the future.
        """
        now = timezone.now()
        question = \
            Question(
                pub_date=now - timezone.timedelta(days=1),
                end_date=now + timezone.timedelta(days=1))
        question.save()
        self.assertTrue(question.can_vote())

    def test_can_vote_with_future_pub_date(self):
        """
        can_vote() returns False for questions whose pub_date
        is in the future.
        """
        now = timezone.now()
        future_question = Question(pub_date=now + timezone.timedelta(days=1),
                                   end_date=now + timezone.timedelta(days=10))
        future_question.save()
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_no_end_date(self):
        """
        can_vote() returns True for questions whose pub_date
        is in the past
        and end_date
        is None.
        """
        now = timezone.now()
        no_end_date_question = \
            Question(pub_date=now - timezone.timedelta(days=1),
                     end_date=None)
        no_end_date_question.save()
        self.assertTrue(no_end_date_question.can_vote())

    def test_can_vote_with_past_end_date(self):
        """
        can_vote() returns False for questions whose end_date
        is in the past.
        """
        now = timezone.now()
        past_question = \
            Question(
                pub_date=now - timezone.timedelta(days=10),
                end_date=now - timezone.timedelta(days=1))
        past_question.save()
        self.assertFalse(past_question.can_vote())
