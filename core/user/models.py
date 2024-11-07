from collections.abc import Iterable
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import model_to_dict
from config.settings import MEDIA_URL, STATIC_URL

from crum import get_current_request

class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['image'] = self.get_image()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]

        return item
        
    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group_id' not in request.session:
                    request.session['group_id'] = groups[0].id
        except:
            pass

    def get_group_from_session(self):
        try:
            request = get_current_request()
            group_id = request.session.get('group_id')
            if group_id:
                return self.groups.get(id=group_id)
            return None
        except:
            return None
