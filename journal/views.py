from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Topic, Entry
from django.urls import reverse_lazy, reverse  
from django import forms
from django.contrib import messages
from collections import Counter
import matplotlib.pyplot as plt
import json
from django.utils.dateparse import parse_date  
from django.views.generic import View, TemplateView
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.db.models import Q  

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

class LockedView(LoginRequiredMixin):
    login_url = "admin:login"

def topic_list(request):
    topics = Topic.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('search_query')

    if start_date:
        topics = topics.filter(created_at__gte=start_date)
    if end_date:
        topics = topics.filter(created_at__lte=end_date)
    
    if search_query:
        entries = Entry.objects.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
        if entries.exists():
            first_entry = entries.first()
            highlighted_content = first_entry.content.replace(
                search_query, f'<span class="highlight">{search_query}</span>'
            )
            first_entry.content = mark_safe(highlighted_content)
            return redirect(reverse('entry_detail', args=[first_entry.id]) + f"?highlight={search_query}")

    return render(request, 'journal/index.html', {'topics': topics})

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content', 'emotion']

def topic_create(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = TopicForm()

    return render(request, 'journal/topic_create.html', {'form': form})

def entry_create(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        emotion = request.POST['emotion']
        Entry.objects.create(topic=topic, title=title, content=content, emotion=emotion)
        return redirect('topic_detail', topic_id=topic_id)
    return render(request, 'journal/entry_create.html', {'topic': topic})

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    entries = Entry.objects.filter(topic=topic_id)

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    search_query = request.GET.get('search_query')

    if start_date:
        start_date = parse_date(start_date)
        entries = entries.filter(created_at__gte=start_date)
    if end_date:
        end_date = parse_date(end_date)
        entries = entries.filter(created_at__lte=end_date)
    if search_query:
        entries = entries.filter(title__icontains=search_query)


    emotion_counts = {}
    for entry in entries:
        emotion = entry.emotion
        if emotion in emotion_counts:
            emotion_counts[emotion] += 1
        else:
            emotion_counts[emotion] = 1


    emotion_counts_json = json.dumps(emotion_counts)

    return render(request, 'journal/topic_detail.html', {
        'topic': topic,
        'entries': entries,
        'emotion_counts': emotion_counts_json
    })

def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    emotions = Entry._meta.get_field('emotion').choices
    return render(request, 'journal/entry_form.html', {'entry': entry, 'emotions': emotions})

class EntryUpdateView(LockedView, SuccessMessageMixin, UpdateView):
    model = Entry
    fields = ["title", "content", "emotion"]
    success_message = "Your entry was updated!"

    def get_success_url(self):
        return reverse_lazy("entry_detail", kwargs={"pk": self.object.pk})

def delete_entry(request):
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        entry = get_object_or_404(Entry, id=entry_id)
        entry.delete()
        return redirect('topic_detail', topic_id=entry.topic.id)
    return HttpResponse(status=405)

class EntryListView(ListView):
    model = Entry
    template_name = 'entry_list.html'
    context_object_name = 'entry_list'

    def topic_detail(request, topic_id):
        request.session['topic_id'] = topic_id

    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        return Entry.objects.filter(topic=topic).order_by("-date_created")

class EntryDetailView(LockedView, DetailView):
    model = Entry
    template_name = 'journal/entry_detail.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        highlight = self.request.GET.get('highlight')
        if highlight:
            entry = self.get_object()
            highlighted_content = entry.content.replace(
                highlight, f'<span class="highlight">{highlight}</span>'
            )
            entry.content = mark_safe(highlighted_content)
            context['entry'] = entry
        return context
        
def entry_statistics(request):
    entries = Entry.objects.all()
    emotions = [entry.emotion for entry in entries]
    emotion_counts = Counter(emotions)

    labels = emotion_counts.keys()
    sizes = emotion_counts.values()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Emotion Distribution in Entries')
    plt.axis('equal')

    chart_image_path = 'journal/static/pie_chart.png'
    plt.savefig(chart_image_path)

    return render(request, 'journal/entry_statistics.html', {'chart_image_path': chart_image_path})

def delete_topic(request):
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        topic = get_object_or_404(Topic, id=topic_id)
        topic.delete()
        return redirect('index')
    return HttpResponse(status=405)

class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return self.render_to_response({'error': 'Invalid username or password.'})

class SignUpView(TemplateView):
    template_name = 'signup.html'

    def get(self, request):
        return self.render_to_response({})

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return self.render_to_response({'error': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return self.render_to_response({'error': 'Username already exists.'})
        if User.objects.filter(email=email).exists():
            return self.render_to_response({'error': 'Email already in use.'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')

def entry_content(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    return JsonResponse({'content': entry.content})
