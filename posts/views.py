from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import FishingReport, Comment
from subnetwork.models import SubNetwork
from django.utils.text import slugify

# Create your views here.


@login_required
def create_report(request):
    if request.method == "POST":
        if request.POST['title'] and request.POST['body']:
            report = FishingReport()
            report.title = request.POST['title']
            report.slug = slugify(report.title)
            report.body = request.POST['body']
            report.sub_network = SubNetwork.objects.get(sub_name=request.POST['sub'])
            report.pub_date = timezone.datetime.now()
            report.author = request.user
            report.save()
            return render(request, 'posts/createreport.html')
    else:
        subnetwork = request.user.subnetwork_set.all()
        return render(request, 'posts/createreport.html',
                      {'subnetwork': subnetwork})


def report_detail(request, pk):
    report = FishingReport.objects.get(id=pk)
    comments = Comment.objects.filter(parent_report=report)
    if request.method == 'POST':
        # A comment was posted
        new_comment = Comment(body=request.POST['comment'])
        new_comment.author = User.objects.get(id=pk)
        new_comment.parent_report = report
        new_comment.save()
    return render(request, 'posts/report_detail.html',
                  {'report': report,
                   'comments': comments,
                   })


def home_page(request, pk):
    search_networks = SubNetwork.objects.filter(followers=pk)
    home_posts = FishingReport.objects.filter(sub_network=search_networks).order_by('-pub_date')
    paginator = Paginator(home_posts, 10)

    page = request.GET.get('page')
    try:
        pag_post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pag_post = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pag_post = paginator.page(paginator.num_pages)
    return render(request, 'posts/posts_home.html', {'home_posts': home_posts,
                                                     'pag_post': pag_post})
