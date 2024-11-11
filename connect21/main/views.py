from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import TemplateView

from groups.models import GroupInvitation, GroupMembership
from main.mixins import TitleMixin


class HomeView(TitleMixin, TemplateView):
    title = 'Connect21 - Главная'
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_groups'] = GroupMembership.objects.filter(user=self.request.user).select_related('group')
            context['incoming_invitations'] = GroupInvitation.objects.filter(receiver=self.request.user, status='pending')
            context['show_create_chat_button'] = True
        return context


class RespondInvitationView(LoginRequiredMixin, View):
    def post(self, request, invitation_id):
        invitation = get_object_or_404(GroupInvitation, id=invitation_id)

        response = request.POST.get('response')
        if response == 'accept':
            invitation.status = 'accepted'
            invitation.save()
            GroupMembership.objects.create(
                user=request.user,
                group=invitation.group
            )
            messages.success(request, "Приглашение принято!")
        elif response == 'decline':
            invitation.status = 'declined'
            invitation.save()
            messages.info(request, "Приглашение отклонено.")

        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def page_not_found(request, exception):
    return render(request, '404.html', status=404, context={'title': 'Connect21 - Страница не найдена'})


class AboutView(TitleMixin, TemplateView):
    title = 'Connect21 - О нас'
    template_name = 'main/about.html'
