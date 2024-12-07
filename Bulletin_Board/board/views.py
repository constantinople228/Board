from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .filters import AdsFilter
from .forms import AdsForm, ReplyForm, SendForm
from .models import Ads, Reply
from django.conf import settings

# Create your views here.


class AdsList(ListView):
    model = Ads
    template_name = 'ads_list.html'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_logged'] = self.request.user.is_authenticated
        context['current_user'] = self.request.user
        context['user_is_staff'] = self.request.user.is_staff
        return context


class AdsCreate(CreateView):
    form_class = AdsForm
    model = Ads
    template_name = 'ads_create.html'
    success_url = reverse_lazy('board:ads_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class AdsUpdate(UpdateView):
    permission_required = 'ads.change_post'
    form_class = AdsForm
    model = Ads
    template_name = 'ads_edit.html'
    context_object_name = 'ads_edit'
    success_url = '/ads/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ads.objects.get(pk=id)


class ReplyAdd(CreateView):
    form_class = ReplyForm
    model = Reply

    template_name = 'reply_add.html'
    context_object_name = 'reply_create'

    success_url = '/ads/'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.post = get_object_or_404(Ads, id=self.kwargs['pk'])
        form.save()
        return redirect('post', reply.post.pk)


@login_required
def profile_view(requset):
    return render(requset, 'registration/profile.html')


class Replies(ListView):
    model = Reply
    template_name = 'replies.html'
    context_object_name = 'replies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Reply.objects.filter(post__post_author_id=self.request.user.pk).order_by('-date_posted')
        context['filter'] = AdsFilter(self.request.GET, queryset, request=self.request.user.pk)
        return context

    def get_queryset(self):
        return Reply.objects.filter(post__author=self.request.user)


def news_send(request):
    if request.method == 'GET':
        form = SendForm()
        return render(request, 'send_mails.html', {'form': form})
    else:
        form = SendForm(request.POST)
        if form.is_valid():
            content_mail = form.cleaned_data.get('content')
            recievers = []
            for user in User.objects.all():
                if user.email != ' ' or user.email != '':
                    recievers.append(user.email)

            html_mail = render_to_string(
                'send_mails_mail.html',
                {
                    'text': content_mail,
                }
            )

            message = EmailMultiAlternatives(
                subject=f'Новость!',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=recievers
            )

            message.attach_alternative(html_mail, 'text/html')
            message.send()

            return redirect('/posts/')


def delete_reply(self, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return redirect('/ads/')


def allow_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.is_allowed = True
    html_mail = render_to_string(
        'reply_sendmail_accepted.html',
        {
            'text': reply.content,
            'post_title': reply.ads.title,
            'post_link': f'http://127.0.0.1:8000/ads/{reply.ads.pk}',
        }
    )

    message = EmailMultiAlternatives(
        subject=f'Ваш отклик был принят',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[reply.author.email]
    )

    message.attach_alternative(html_mail, 'text/html')
    message.send()
    reply.save()
    return redirect('/ads/')


def delete_ads(self, pk):
    post = Ads.objects.get(id=pk)
    post.delete()
    return redirect('/ads/')


def load_more_ads(request):
    page = int(request.GET.get('page', 1))
    try:
        ads_list = Ads.objects.all().order_by()
        paginator = Paginator(ads_list, 10)
        ads = paginator.get_page(page)
        html = render_to_string('ads_list_fragment.html', {'ads': ads})
        return JsonResponse({'html': html})
    except (PageNotAnInteger, EmptyPage):
        return JsonResponse({'error': 'Нет больше объявлений'}, status=404)


