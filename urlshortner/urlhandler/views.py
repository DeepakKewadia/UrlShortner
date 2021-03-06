from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import shorturl

# Create your views here.

@login_required(login_url='/login')
def dashboard(request):
    usr = request.user
    urls = shorturl.objects.filter(user = usr)
    return render(request, 'dashboard.html', { 'urls':urls })

@login_required(login_url='/login')
def generate(request):
    if request.method == "POST":
        if request.POST['original'] and request.POST['short']:
            usr = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shorturl.objects.filter(short_query = short)
            if not check:
                newurl = shorturl(
                    user = usr,
                    original_url = original,
                    short_query = short,
                )
                newurl.save()
                return redirect('/dashboard')
            else:
                messages.error(request, "Already Exits")
                return redirect('/dashboard')
            
        elif request.POST['original']:
            #generate randomly
            pass
        else:
            return redirect('/dashboard')
    else:
        messages.error(request, "Empty Fields")
        return redirect('/dashboard')
