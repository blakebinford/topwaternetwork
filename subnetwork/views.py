from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User

from .models import SubNetwork
from posts.models import FishingReport


# Create your views here.


def sub(request, sub_name):
    subnetwork = SubNetwork.objects.get(sub_name=sub_name)
    fishing_report = FishingReport.objects.filter(sub_network=subnetwork.id).order_by('-pub_date')

    paginator = Paginator(fishing_report, 10)

    page = request.GET.get('page')
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    return render(request, 'subnetwork/sub.html', {'subnetwork': subnetwork,
                                                   'reports': reports})


def all_subs(request):
    if request.method == 'POST':
        sub_name = SubNetwork.objects.get(sub_name=request.POST['sub_form'])
        return redirect('/sub/{}'.format(sub_name))
    else:
        subnetwork = SubNetwork.objects.all()
        paginator = Paginator(subnetwork, 10)

        page = request.GET.get('page')
        try:
            subs = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            subs = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            subs = paginator.page(paginator.num_pages)

        return render(request, 'subnetwork/all_subs.html', {'subnetwork': subnetwork,
                                                            'subs': subs})


def follow(request, pk):
    if request.method == 'POST':
        report = SubNetwork.objects.get(id=pk)
        report.followers.add(request.user)
        report.save()
        return redirect('/sub/{}/'.format(report.sub_name))
