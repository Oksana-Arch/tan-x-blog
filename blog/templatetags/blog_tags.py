from django import template
from django.utils.safestring import mark_safe
from ..models import Post, Comment
import markdown

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

# @register.simple_tag(name="next_post")
# def get_next_post():
#     return Post.objects.get_next_by_publish(is_next=True)

# post.get_previous_by_publish(is_next=False)

# @register.inclusion_tag('blog/includes/post_comments.html', takes_context=True)
# def posts_list_recent(context):
#     posts = Post.published.all()[:3]
#     comments = Comment.objects.all()[:3]
#     return {
#         'post_list_recent': posts,
#         'comment_list_resent': comments,
#     }
@register.simple_tag()
def post_list_resent():
    posts = Post.published.all()[:4]
    return posts

@register.simple_tag()
def comments_list():
    comments = Comment.objects.all().order_by('-pub_date')[:4]
    return comments