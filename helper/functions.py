from Users.models import UserDetail


def get_user_name(user):
    user_detail = UserDetail.objects.get(user=user)
    return user_detail.nick_name