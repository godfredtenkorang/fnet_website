from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        """ Prevents blocked users from authenticating """
        return super().user_can_authenticate(user) and not user.is_blocked