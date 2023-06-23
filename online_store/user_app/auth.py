from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(email=username) | Q(username=username))
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
