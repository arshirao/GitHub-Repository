from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import LoginForm
from .models import Choice, Question,User


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


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    ... # same as above, no changes needed.
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class Vote(generic.CreateView):
    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, pk=kwargs['question_id'])
        try:
            selected_choice = question.choice_set.get ( pk=request.POST[ 'choice' ] )
        except (KeyError , Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render ( request , 'polls/detail.html' , {
                'question': question ,
                'error_message': "You didn't select a choice." ,
            } )
        else:
            selected_choice.votes += 1
            selected_choice.save ()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect ( reverse ( 'polls:results' , args=(question.id ,) ) )


class FormView(generic.FormView):
    model = User
    template_name = 'polls/forms.html'

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            form.save()
            return render(request,self.template_name,{'form':form,'name':name,'username':username,'password':password})

        return HttpResponseRedirect(reverse('polls:form'))

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request,self.template_name,{'form':form})
