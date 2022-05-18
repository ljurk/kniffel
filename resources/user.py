from . import BaseResource
import models.user

class UserResource(BaseResource):
    def __init__(self):
        self.model = models.user.User
        super().__init__()
