from django.shortcuts import render

from .models import Users


def index(request):

    users = Users.objects.all()

    context = {
        'stat1': 'Users',
        'count1': Users.objects.count(),
        'stat2': 'Email addresses',
        #'count2': Users.objects.raw('SELECT SUM(LENGTH(email) - LENGTH(REPLACE(email, ',', '')) + 1) AS listCount FROM webapp_users;'),
        'count2': Users.objects.exclude(email__isnull=True).count() + Users.objects.filter(email__contains=',').count(),
        'stat3': 'Phone numbers',
        'count3': Users.objects.exclude(phone__isnull=True).count() + Users.objects.filter(phone__contains=',').count(),
        'stat4': 'Locations',
        'count4': Users.objects.exclude(locations__isnull=True).count(),
        'users': users,
        'cols': [f.name for f in Users._meta.get_fields()][:-2]
    }

    return render(request, 'browse/index.html', context)
