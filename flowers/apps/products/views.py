import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import register
from django.views import View
from django.views.generic import DetailView

from apps.products.forms import ReviewForm, CommentForm, LoginUserForm
from apps.products.models import Products, Reviews, Comments
from apps.products.services import base_context, grade_product, fill_form, change_review, change_comment, \
    show_our_stores


def about_us(request):
    return render(request, 'products/aboutus.html', context={'title': 'О нас', 'form': LoginUserForm})


class BaseProduct(DetailView):
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        return base_context(self, super().get_context_data(**kwargs))


@register.filter
def filter_user(req, user):
    return req.filter(user=user)


class ShowReviewsView(BaseProduct):
    model = Products
    template_name = 'products/reviews.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = super(BaseProduct, self).get_context_data(**kwargs)
        context.update(context_new)
        context.update({'reviews': Reviews.objects.filter(product=context['product'].id).order_by('-date_uploaded')})
        return context


class ShowCommentsView(BaseProduct):
    model = Products
    template_name = 'products/comments.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context_new = super(BaseProduct, self).get_context_data(**kwargs)
        context.update(context_new)
        context.update({'comments': Comments.objects.filter(product=context['product'].id).order_by('-date')})
        return context
    

def grade_product_view(request):
    grade_product(request.user, request.GET.get('grade_product'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddReviews(View):

    @staticmethod
    def post(request, pk):
        fill_form(ReviewForm(request.POST), Products.objects.get(pk=pk), request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddComments(View):

    @staticmethod
    def post(request, pk):
        fill_form(CommentForm(request.POST), Products.objects.get(pk=pk), request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_review(request, pk):
    Reviews.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_comment(request, pk):
    Comments.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_review_view(request, product_id, review_id):
    change_review(product_id, review_id, Reviews, ReviewForm(request.POST))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_comment_view(request, product_id, comment_id):
    change_comment(product_id, comment_id, Comments, CommentForm(request.POST))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def our_stores(request):
    answer = request.COOKIES.get('answer')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    context = show_our_stores(answer, ip)
    return render(request, 'products/our_stores.html', context)
