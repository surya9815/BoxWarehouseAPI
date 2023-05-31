from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.
#  cuboid(which have length, breadth and height) -> store employee -> creator

class CustomUser(AbstractUser):
    is_staff = models.BooleanField(default=True)

class Box(models.Model):
    length = models.FloatField()
    breadth = models.FloatField()
    height = models.FloatField()
    area = models.FloatField(editable=False)
    volume = models.FloatField(editable=False)
    creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE,editable=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        self.area = self.length * self.breadth
        self.volume = self.length * self.breadth * self.height
        super().save(*args, **kwargs)

    # Overriding the save method in the Box model to prevent  
    # staff users from modifying the creator and created_at fields when updating a box.
    # def can_update(self,user):
    #     #Allow updating the box if the user is a staff member
    #     return user.is_staff    # returns True or False
    
    # def can_delete(self,user):
    #     #allow updating only when user is creator and a staff member
    #     return user.is_staff and self.creator == user

    # @classmethod
    # def get_user_boxes(cls,user):
    #     #Return the boxes created by staff user
    #     if user.is_staff:
    #         return cls.objects.filter(creator=user)
    #     else:
    #         return cls.objects.none()





