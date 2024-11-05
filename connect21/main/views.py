from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from groups.models import GroupMembership, GroupInvitation
from django.contrib import messages


def home_page(request):
    user_groups = []  # 🤏 чут чут костылей
    if request.user.is_authenticated:
        user_groups = GroupMembership.objects.filter(user=request.user).select_related('group')
        incoming_invitations = GroupInvitation.objects.filter(receiver=request.user, status="pending")

        return render(request, 'main/home.html', {
            'user_groups': user_groups,
            'incoming_invitations': incoming_invitations,
        })
    return render(request, 'main/home.html')


@login_required
def respond_invitation(request, invitation_id):
    invitation = get_object_or_404(GroupInvitation, id=invitation_id)

    if request.method == "POST":
        if request.POST.get('response') == 'accept':
            invitation.status = 'accepted'
            invitation.save()

            GroupMembership.objects.create(
                user=request.user,
                group=invitation.group
            )
            messages.success(request, "Приглашение принято!")
        elif request.POST.get('response') == 'decline':
            invitation.status = 'declined'
            invitation.save()
            messages.info(request, "Приглашение отклонено.")

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def about(request):
    return render(request, 'main/about.html')
