import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from polls.models import Question, Choice
from django.utils import timezone

q1 = Question(question_text="Django nədir?", pub_date=timezone.now())
q1.save()
q1.choice_set.create(choice_text='Web framework', votes=0)
q1.choice_set.create(choice_text='Proqramlaşdırma dili', votes=0)
q1.choice_set.create(choice_text='Verilənlər bazası', votes=0)

print("Suallar əlavə edildi!")