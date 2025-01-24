from django.shortcuts import render, redirect, get_object_or_404
from .models import Question
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import QuestionForm
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# API Key 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 프롬프트 명령
prompt = "You are a very scary computer teacher."

# 초기 대화 설정
messages = [{"role": "sytem", "content": prompt}]

# 질문 리스트
def question_list(request):
    questions = Question.objects.all().order_by('-id')
    context = {
        'questions':questions
    }
    return render(request, 'chatbot/question_list.html', context)

# 질문하기
@login_required
@require_http_methods(['GET','POST'])
def question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit = False)
            question.user = request.user
            response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": "You are a tour guide in Korea"}, # 프롬프트 명령
                {"role": "user", "content" : question.question} # 사용자 입력
                ]
            )
            question.answer = response['choices'][0]['message']['content']
            question.save()
            return redirect('chatbot:answer', question.pk)
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'chatbot/question.html', context)

def answer(request,pk):
    question = get_object_or_404(Question, pk=pk)
    answer = question.answer
    context = {
        'question':question,
        'answer':answer,
    }
    return render(request, 'chatbot/answer.html', context)