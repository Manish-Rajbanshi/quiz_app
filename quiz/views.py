from django.shortcuts import render, redirect
from .models import Question

# Store static questions in a global variable (in production, this should ideally use a database)
QUESTIONS = [
    {'question': 'What is the official name of the Constitution of Nepal?', 
     'options': ['Constitution of the Kingdom of Nepal', 'Interim Constitution of Nepal', 'Constitution of Nepal 2072', 'Nepal Democratic Constitution'], 
     'answer': 'Constitution of Nepal 2072'},
    
    {'question': 'In which year was the Constitution of Nepal promulgated?', 
     'options': ['2013', '2015', '2017', '2019'], 
     'answer': '2015'},
    
    {'question': 'How many articles are there in the Constitution of Nepal?', 
     'options': ['275', '299', '304', '308'], 
     'answer': '308'},
    
    {'question': 'What is the form of government in Nepal according to its Constitution?', 
     'options': ['Monarchy', 'Federal Democratic Republic', 'Unitary Parliamentary', 'Socialist Republic'], 
     'answer': 'Federal Democratic Republic'},
    
    {'question': 'Which body has the power to amend the Constitution of Nepal?', 
     'options': ['Supreme Court', 'House of Representatives', 'Constitutional Council', 'Federal Parliament'], 
     'answer': 'Federal Parliament'},
    
    {'question': 'What is the national language of Nepal as per the Constitution?', 
     'options': ['English', 'Hindi', 'Nepali', 'Maithili'], 
     'answer': 'Nepali'},
    
]

def index(request):
    return render(request, 'index.html')

def quiz(request):
    if 'current_question' not in request.session:
        request.session['current_question'] = 0
        request.session['score'] = 0

    # Combine questions from both the database and the static list
    questions_from_db = list(Question.objects.all())
    all_questions = questions_from_db + QUESTIONS
    current_question_index = request.session['current_question']

    if current_question_index >= len(all_questions):  # Quiz complete
        score = request.session['score']
        total = len(all_questions)
        request.session.flush()
        return render(request, 'result.html', {'score': score, 'total': total})

    question = all_questions[current_question_index]

    if request.method == 'POST':
        selected_answer = request.POST.get('answer')
        if selected_answer == question['answer'] if isinstance(question, dict) else question.correct_answer:
            request.session['score'] += 1
        request.session['current_question'] += 1
        return redirect('quiz')

    # Render either a dictionary or model-based question
    if isinstance(question, dict):
        return render(request, 'quiz.html', {
            'question': question,
            'current_question': current_question_index + 1,
            'total_questions': len(all_questions),
        })
    else:
        return render(request, 'quiz.html', {
            'question': {
                'question': question.question_text,
                'options': [question.option1, question.option2, question.option3, question.option4],
            },
            'current_question': current_question_index + 1,
            'total_questions': len(all_questions),
        })

def add_question(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        options = [
            request.POST.get('option1'),
            request.POST.get('option2'),
            request.POST.get('option3'),
            request.POST.get('option4'),
        ]
        answer = request.POST.get('answer')

        if question_text and options and answer:
            # Save the new question to the database
            Question.objects.create(
                question_text=question_text,
                option1=options[0],
                option2=options[1],
                option3=options[2],
                option4=options[3],
                correct_answer=answer,
            )
            return redirect('quiz')  # Redirect to quiz after adding a question

    return render(request, 'add.html')
