from .user import Users, Roles
from mongoengine.errors import NotUniqueError

def drop_all():
    for usr in Users.objects:
        usr.delete()
    for role in Roles.objects:
        role.delete()

def create_all():
    preset_roles = ['admin', 'editor', 'reader']
    k = 0
    for role in preset_roles:
        try:
            Roles(key=k, role=role).save()
            k += 1
        except(NotUniqueError):
            pass