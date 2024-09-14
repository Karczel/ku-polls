"""Module for polls app views."""

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

import logging
from django.contrib.auth.signals import user_logged_in, \
    user_logged_out, user_login_failed
from django.dispatch import receiver

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question, Vote

from ku_polls import settings

logger = logging.getLogger('polls')


def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class IndexView(generic.ListView):
    """Class based view for Index."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.

        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Class based view for viewing a poll."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(
            pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        """Apply is_published and can_vote methods."""
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        user = self.request.user

        context['is_published'] = question.is_published()
        context['can_vote'] = question.can_vote()

        user_vote = Vote.objects.filter(
            user=user,
            choice__question=question).first()
        context['previous_choice'] = user_vote.choice if user_vote else None

        return context

    def get(self, request, *args, **kwargs):
        """
        Return appropriate details page.

        If you cannot get page at Question Index, it will raise Http404 error.
        If you got into questions you're not allowed to vote yet,
        you'll be redirected to index page.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
            if not question.is_published():
                logger.debug(f"Poll '{question.question_text}' "
                             f"is not opened yet.")
                messages.info(request, f"'{question.question_text}' "
                                       f"poll is not opened yet.")
                return HttpResponseRedirect(reverse('polls:index'))
            if not question.can_vote():
                logger.debug(f"Poll '{question.question_text}' "
                             f"is closed.")
                messages.info(request,
                              f"'{question.question_text}' "
                              f"poll is closed.")
                return HttpResponseRedirect(reverse('polls:index'))
        except Http404:
            logger.error("Invalid page exception")
            messages.error(request,
                           "There is no Question with this ID")
            return HttpResponseRedirect(reverse('polls:index'))

        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """Class based view for results."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Vote for a choice on a question (poll)."""
    user = request.user
    ip_addr = get_client_ip(request)

    if not user.is_authenticated:
        # return redirect('login')
        # or, so the user comes back here after login...
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")
    else:
        print("current user is", user.id, "login", user.username)
        print("Real name:", user.first_name, user.last_name)
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, "Voting is closed.")
        return HttpResponseRedirect(reverse('polls:index'))

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form. with an error message.
        logger.error(f"{user.username} from {ip_addr} didn't choose a vote")
        messages.error(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {
            'question': question,
        })

    existing_vote = Vote.objects.filter(
        user=user,
        choice__question=question).first()
    if existing_vote:
        if existing_vote.choice != selected_choice:
            existing_vote.delete()
            current_vote = Vote.objects.create(
                user=user,
                choice=selected_choice)
            current_vote.save()
    else:
        current_vote = Vote.objects.create(
            user=user,
            choice=selected_choice)
        current_vote.save()
        # Always return an HttpResponseRedirect
        # after successfully dealing
        # with POST data. This prevents data from
        # being posted twice if a user hits the Back button.
    logger.info(
        f"{user.username} from {ip_addr} submits vote "
        f"{selected_choice.choice_text} "
        f"in {question.question_text}.")
    messages.success(request,
                     f"Your vote for '{question}' was successfully recorded.")
    return HttpResponseRedirect(
        reverse(
            'polls:results',
            args=(question.id,)))


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # get named fields from the form data
            username = form.cleaned_data.get('username')
            # password input field is named 'password1'
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            logger.info(f"{user.username} successfully logged in")
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
        else:
            messages.error(request, "This form is invalid")
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """Logger records a log if a user successfully logged in."""
    ip_addr = get_client_ip(request)

    logger.info('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip_addr
    ))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """Logger records a log if a user successfully logged out."""
    ip_addr = get_client_ip(request)

    logger.info('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip_addr
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    """Logger records a log if there was a failed login with a warning."""
    logger.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))
