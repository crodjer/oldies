from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from movie.models import *
from django.utils import simplejson
from django.template import RequestContext

def list_movie(request):
    movies = Movie.objects.all().order_by('name')
    return render_to_response('movie/list_movies.html', {'movies':movies}, context_instance=RequestContext(request))

def movie_details(request, movie_id):
    movie = Movie.objects.get(pk = movie_id)
    return render_to_response('movie/movie_details.html', {'movie':movie}, context_instance=RequestContext(request))

def saving(request):
    request.session['status'] = "Processing the input"
    try:
        addtype =  request.session['add_type']
        del request.session['add_type']
        if addtype == 'manual':
            del request.session['imdb_url']
            del request.session['forum_url']
        elif addtype == 'page':
            del request.session['forum_page_url']
            del request.session['forum_movie_regex']
        else:
            del request.session['forum_url']
    except KeyError:
        pass
    if request.method == "POST": 
        request.session['add_type'] = request.POST['add_type']
        if request.POST['add_type'] == 'manual':
            request.session['forum_url'] = request.POST['forum_url']
            request.session['imdb_url'] = request.POST['imdb_url']
        elif request.POST['add_type'] == 'page':
            request.session['forum_page_url'] = request.POST['forum_page_url']
            request.session['forum_movie_regex'] = request.POST['forum_movie_regex']
        else:
            request.session['forum_url'] = request.POST['forum_url']
    return HttpResponseRedirect('/save/')
    return render_to_response('movie/saving.html',context_instance=RequestContext(request))

def save(request):
    try:
        request.session['add_type']
    except KeyError:
        from time import sleep
        print "Will sleep for 5 seconds......"
        sleep(5)
        return HttpResponse('Invalid Access')
    if request.session['add_type'] == 'manual':
        down_info = manual_add_download_info(request.session['imdb_url'],request.session['forum_url'], request = request)
        if not down_info:
            return render_to_response('movie/no_new_info.html')
        else:
            down_infos = [down_info]
    elif request.session['add_type'] == 'page':
        down_infos = add_page(request.session['forum_page_url'], request.session['forum_movie_regex'], request = request)
        if not down_infos:
            return render_to_response('movie/no_new_info.html')
    else:
        down_info = add_download_info(request.session['forum_url'], request = request)
        if not down_info:
            return render_to_response('movie/no_new_info.html')
        else:
            down_infos = [down_info]
    try:
        del request.session['forum_url']
        if request.session['add_type'] == 'manual':
            del request.session['imdb_url']
        del request.session['add_type']
    except:
        pass
    return render_to_response('movie/save_result.html',{'down_infos':down_infos}, context_instance=RequestContext(request))

def save_status(request):
    try:
        status = request.session['status']
        j = simplejson.dumps(status)
    except KeyError:
        j = simplejson.dumps(False)
    return HttpResponse( j, mimetype='application/javascript' )

def search(request):
    query = request.POST.get('query', '') or request.GET.get('query', '') 
    is_ajax = request.POST.get('is_ajax', '')
    movies = Movie.objects.filter(name__istartswith = query).all().order_by('-rating')
    other_movies = Movie.objects.exclude(name__istartswith = query).filter(name__icontains = query).all().order_by('-rating')
    if is_ajax:
        result = []
        for movie in movies[:15]:
            result.append({'name':movie.name, 'url':movie.get_absolute_url(), 'highlighted':False})
        for movie in other_movies[:15]:
            if len(result)<=15:
                result.append({'name':movie.name, 'url':movie.get_absolute_url(),'highlighted':False})
            else:
                break
        if not result:
            result = None
        j = simplejson.dumps(result)
        return HttpResponse(j, mimetype='application/javascript')
    elif query:
        return render_to_response('movie/search_result.html', {'movies':movies, 'other_movies':other_movies,'query':query}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/')
