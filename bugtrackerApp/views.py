from django.shortcuts import render

posts = [
    {
        'creator': 'Dev1',
        'title:': 'dumb bug',
        'content': 'This dumb bug occured',
        'date_posted': 'August 1, 2000'
    },

    {
        'creator': 'Dev1',
        'title:': 'dumb bug 2',
        'content': 'This dumb bug occured',
        'date_posted': 'August 6, 2000'
    },

    {
        'creator': 'Dev2',
        'title:': 'dumb bug 3',
        'content': 'This silly bug occured',
        'date_posted': 'August 20, 2000'
    }
]


def home(request):
    # values inside context will be available to the templates
    context = {
        'posts': posts
    }
    return render(request, 'bugtrackerApp/home.html', context)

def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'bugtrackerApp/about.html', context)


