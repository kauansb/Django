from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question
from django.views import generic

class IndexView(generic.ListView):
    template_name = "enquetes/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Retorna as últimas 5 perguntas publicadas (não incluindo os definidos como publicado no futuro)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "enquetes/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "enquetes/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Reexibir o formulário de votação da pergunta.
        return render(
            request,
            "enquetes/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Sempre retorne um HttpResponseRedirect depois de negociar com sucesso
        # com dados POST. Isso evita que os dados sejam postados duas vezes se um usuário pressionar o botão Voltar.
        return HttpResponseRedirect(reverse("enquetes:results", args=(question.id,)))