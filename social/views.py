from rest_framework.viewsets import ModelViewSet

from social.models import User


class UserView(ModelViewSet):
    """
        A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def user_signup(*args, **kwargs):
        pass

def user_signup(*args, **kwargs):
    pass

def user_login(*args, **kwargs):
    pass

def create_post(*args, **kwargs):
    pass

def like_post(*args, **kwargs):
    pass

def unlike_post(*args, **kwargs):
    pass