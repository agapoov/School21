from celery import shared_task
from .models import GroupInvitation


@shared_task(name='delete all declined group invitations')
def delete_all_invitations():
    declined_invites = GroupInvitation.objects.filter(status='declined')
    count, _ = declined_invites.delete()
    return f'Удалено {count} отклоненных приглашений.'
