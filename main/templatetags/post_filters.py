from django import template
from main.models import Post

register = template.Library()

@register.filter
def user_has_liked(post, user):
    return post.user_has_liked(user)