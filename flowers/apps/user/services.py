from django.contrib.auth.models import User
from django.http import Http404

from apps.user.models import UserLike
from apps.products.models import Products, Comments


def reply_comment(form, user, pk_product, pk_comment):
    product = Products.objects.get(id=pk_product)
    comment = Comments.objects.get(id=pk_comment)
    if form.is_valid():
        form = form.save(commit=False)
        form.user = user
        form.product = product
        form.comment = comment
        form.save()
        print("ok")
    else:
        print("no")


def delete_user(user_id):
    try:
        u = User.objects.get(pk=user_id)
        u.delete()
    except Exception:
        raise Http404


def like_product(like, user):
    obj, create = UserLike.objects.get_or_create(user=user, product_id=like)
    if not create:
        obj.delete()
