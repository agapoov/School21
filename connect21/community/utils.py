from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector)

from groups.models import GroupInvitation, GroupMembership
from users.models import User


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return User.objects.filter(id=int(query))

    vector = SearchVector('username', 'additional_info', 'interests', 'first_name', 'last_name', 'surname', 'tg_username')
    query = SearchQuery(query)

    return User.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank")


def check_and_invite_user(request, invited_user, group):
    if GroupMembership.objects.filter(group=group, user=invited_user).exists() or \
            GroupInvitation.objects.filter(group=group, receiver=invited_user, status="pending").exists():
        return False

    GroupInvitation.objects.create(
        group=group,
        sender=request.user,
        receiver=invited_user,
        status="pending"
    )
    return True
