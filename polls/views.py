from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Choice, Question, Vote

# messages.set_level(request, messages.DEBUG )
# or, reset it to the default
# messages.set_level( request, None )

# CRITICAL = 50
# messages.add_message(request, CRITICAL, "Database error occurred.")
# messages.info(request, "Your vote was recorded", extra_tags='alert')


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    """Class based view for viewing a poll."""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        """Apply is_published and can_vote methods"""
        context = super().get_context_data(**kwargs)
        question = self.object

        context['is_published'] = question.is_published()
        context['can_vote'] = question.can_vote()

        return context

    def get(self, request, *args, **kwargs):
        """If you cannot get page at Question Index,
        get_object_or_404() will raise Http404 error"""
        try:
            get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            messages.error(request, "There is no Question with this ID")
            return HttpResponseRedirect(reverse('polls:index'))
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    """Vote for a choice on a question (poll)."""
    user = request.user
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
        messages.error(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {
            'question': question,
        })

    existing_vote = Vote.objects.filter(user=user, choice__question=question).first()
    if existing_vote:
        if existing_vote.choice != selected_choice:
            existing_vote.delete()
            current_vote = Vote.objects.create(user=user, choice=selected_choice)
    else:
        current_vote = Vote.objects.create(user=user, choice=selected_choice)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    current_vote.save()
    messages.success(request, "Your vote was successfully recorded.")
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
            user = authenticate(username=username,password=raw_passwd)
            login(request, user)
            return redirect('polls:index')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        # create a user form and display it the signup page
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})