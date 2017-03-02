from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import FishingReport, Comment
from subnetwork.models import SubNetwork
from django.utils.text import slugify
from django.core.mail import send_mail

# Create your views here.


@login_required
def create_report(request):
    if request.method == "POST":
        if not None:
            try:
                if request.POST['title'] and request.POST['body']:
                    report = FishingReport()
                    report.title = request.POST['title']
                    report.slug = slugify(report.title)
                    report.body = request.POST['body']
                    report.sub_network = SubNetwork.objects.get(sub_name=request.POST['sub'])
                    report.pub_date = timezone.datetime.now()
                    report.author = request.user
                    report.save()
                    return render(request, 'posts/report_detail.html', {'report': report})
                else:
                    subnetwork = request.user.subnetwork_set.all()
                    return render(request, 'posts/createreport.html',
                                  {'subnetwork': subnetwork,
                                   'error': 'Please fill out the entire form.'})
            except:
                subnetwork = request.user.subnetwork_set.all()
                return render(request, 'posts/createreport.html',
                              {'subnetwork': subnetwork,
                               'error': 'Please fill out the entire form.'})

    else:
        subnetwork = request.user.subnetwork_set.all()
        return render(request, 'posts/createreport.html',
                      {'subnetwork': subnetwork})


def report_detail(request, pk):
    report = FishingReport.objects.get(id=pk)
    comments = Comment.objects.filter(parent_report=report)
    user = request.user
    if report.votes.exists(user.id):
        user_liked = True
    else:
        user_liked = False
    if request.method == 'POST':
        if request.user.is_authenticated:
            # A comment was posted
            new_comment = Comment(body=request.POST['comment'])
            if new_comment.body != '':
                new_comment.author = user
                new_comment.parent_report = report
                new_comment.save()
                email_body = 'You have a new comment on your post {}.'.format(report.title)
                send_mail('Thank you for signing up with Top Water Network!', email_body, 'noreply@topwaternetwork.com',
                          [report.author.email], fail_silently=False)
            else:
                return render(request, 'posts/report_detail.html',
                              {'report': report,
                               'comments': comments,
                               'user_liked': user_liked
                               })
        else:
            return render(request, 'accounts/login.html', {'error': 'You must be signed in to do that'})
    return render(request, 'posts/report_detail.html',
                  {'report': report,
                   'comments': comments,
                   'user_liked': user_liked
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


def front_page(request):
    all_posts = FishingReport.objects.all().order_by('-pub_date')
    paginator = Paginator(all_posts, 15)

    page = request.GET.get('page')
    try:
        paginate = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginate = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginate = paginator.page(paginator.num_pages)

    return render(request, 'posts/frontpage.html',
                  {'all_posts': all_posts,
                   'paginate': paginate})


def report_star(request, pk):
    if request.user.is_authenticated:
        report = FishingReport.objects.get(pk=pk)
        user = request.user.id
        comments = Comment.objects.filter(parent_report=report)
        if report.votes.exists(user):
            report.votes.delete(user)
            user_liked = False
            return render(request, 'posts/report_detail.html', {'user_liked': user_liked,
                                                                'report': report,
                                                                'comments': comments})
        else:
            report.votes.up(user)
            user_liked = True
            return render(request, 'posts/report_detail.html', {'user_liked': user_liked,
                                                                'report': report,
                                                                'comments': comments})
    else:
        return render(request, 'accounts/login.html', {'error': 'You must be signed in to do that'})
