import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = \
            timezone.now() - datetime.timedelta(
                hours=23,
                minutes=59,
                seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.was_published_recently())

    def test_is_published_in_the_future(self):
        """is_published() returns False for questions whose pub_date is in the future."""
        now = timezone.now()
        future_question = Question(pub_date=now + timezone.timedelta(days=30))
        self.assertFalse(future_question.is_published())

    def test_is_published_in_the_present(self):
        """is_published() returns True for questions whose pub_date is in the present."""
        now = timezone.now()
        default_pub_date_question = Question(pub_date=now)
        self.assertTrue(default_pub_date_question.is_published())

    def test_is_published_in_the_past(self):
        """is_published() returns True for questions whose pub_date is in the past."""
        now = timezone.now()
        past_question = Question(pub_date=now - timezone.timedelta(days=30))
        self.assertTrue(past_question.is_published())


def create_question(question_text, days):
    """
    Create a question with the given `question_text`.
    And published the given number of `days` offset to now.
    (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = \
            create_question(
                question_text='Future question.',
                days=5)
        url = reverse('polls:detail',
                      args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = \
            create_question(
                question_text='Past Question.',
                days=-5)
        url = reverse('polls:detail',
                      args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,
                            past_question.question_text)
