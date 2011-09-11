from django.db import models
import mechanize, re
from besoup import BeautifulSoup
br = mechanize.Browser()
##Defines a general movie with imdb info

    
    
class Movie(models.Model):    
    name = models.CharField('Name', max_length = 100) 
    imdb_url = models.URLField('IMDB url' ,verify_exists=True, unique=True)
    image =   models.URLField('Image Url' ,verify_exists=True, unique=True)
    plot = models.TextField('Plot', max_length = 200, blank = True) 
    year = models.CharField('Year', max_length = 10)
    release_date = models.CharField('Release Date', max_length = 200, blank = True)
    rating = models.FloatField('Rating')
    director = models.CharField('Director', max_length = 200)
    writers = models.CharField('Writer', max_length = 200)
    stars = models.TextField('Stars')
    genre = models.CharField('Genre', max_length = 200)
    time = models.DateTimeField('Time', auto_now=True)
    firstchar = models.CharField('First Character', max_length = 10)
    def __unicode__(self):
        return self.name
    #Scrapping info from imdb
    
    def fetch_imdb_info(self):
        print 'Fetching info from IMDB......'        
        response = br.open(self.imdb_url)
        html = str(response.read())                    
        soup = BeautifulSoup(html)
        self.soup = soup
        heading  = soup.h1
        try:
            self.year = heading.span.a.text
        except AttributeError:
            self.year = ""
        subtree = heading.span
        subtree.extract()
        self.name = heading.text.replace("&#x22;", "")
        director_div = soup.find('h4',{'class':'inline'}, text=re.compile(r'Director')).parent.parent        
        self.director = director_div.a.text
        writers_div = soup.find('h4',{'class':'inline'}, text=re.compile(r'Writer')).parent.parent        
        trash = writers_div.find('a', href=re.compile('fullcredits'))
        trash.extract()
        writers=[a.text for a in writers_div.findAll('a')]        
        self.writers = ', '.join(writers)
        stars_div = soup.find('h4',{'class':'inline'}, text=re.compile(r'Star')).parent.parent
        stars = [a.text for a in stars_div.findAll('a')]
        self.stars = ', '.join(stars)
        infobar = soup.find('div', {'class':'infobar'})
        try:
            self.release_date = infobar.find('a', href=re.compile(r'releaseinfo')).text.replace('\n',' ').replace('&nbsp;', ' ')
        except AttributeError:
            pass
        genres = [a.text for a in infobar.findAll('a', href=re.compile(r'genre'))]
        self.genre = ', '.join(genres)
        star_box = soup.find('div', {'class':'star-box'})
        rating_div = star_box.find('span', {'class':'rating-rating'})
        trash = rating_div.find('span')
        trash.extract()        
        self.plot = star_box.findNextSibling('p').findNextSibling('p').text
        self.rating = float(rating_div.text)
        try:
            image_url = soup.find('img',src=re.compile('ia.media-imdb.com'))['src']
            while True:
                try:
                    self.fetch_image(image_url)
                    break
                except:
                    pass
        except TypeError:
            pass

    def printself(self):
        print '\
            Name:\t\t%s\n\
            Rating:\t\t%2.1f\n\
            Year:\t\t%s\n\
            Release Date:\t%s\n\
            Director:\t\t%s\n\
            Writers:\t\t%s\n\
            Genre:\t\t%s\n\
            Stars:\t\t%s\n\
            Plot:\t\t%s\n'  %(self.name,
        self.rating,self.year,
        self.release_date, self.director,
        self.writers, self.genre,self.stars,
        self.plot
        )
    
    def fetch_image(self,image_url):
        print 'Uploading Image......'
        br.open('http://imghost.rohanjain.in/')
        br.select_form(name="url")
        br["url"] = image_url
        response = br.submit()
        for link in br.links(url_regex="http://img\w+.imageshack.us/img\w+/\w+/\w+"):
            break
        self.image = link.url
        return True
    
    def get_absolute_url(self):
        return '/%d/' %(self.id)
        
#Makes a new movie object from the imdb info provided
def new_movie(imdb_url):
    pattern = re.compile('imdb.com/title/tt\d{7}')
    search = re.search(pattern, imdb_url)
    if search:
        imdb_url = search.group()
        imdb_url = 'http://www.' + imdb_url
        imdb_url = imdb_url + '/'
        try:
            movie =  Movie.objects.get(imdb_url = imdb_url)
            movie.printself()
        except Movie.DoesNotExist:
            movie = Movie(imdb_url = imdb_url)
            if  movie.fetch_imdb_info():
                movie.save()
                movie.printself()
            else:
                return None
        return movie
    else:
        return None

def update_session(request, movie, message = ''):
    if request:
        if message:
            message = str(", " + message)
        request.session['status'] = str("Processing Movie - " + movie.name + message)
        request.session.save()
        print request.session['status'] + "\n"

#Has the info required for downloading and download links for movie         
class DownloadInfo(models.Model):
    movie = models.ForeignKey(Movie)
    forum_url = models.URLField('Forum url' ,verify_exists=True, max_length=250, unique=True)
    download_links = models.TextField('Download Links')
    our_rating = models.IntegerField('Our Rating')  
    def __unicode__(self):
        return self.forum_url
    #Checking the forum page for imdb info
    def process_forum_page(self,forum_url, request = None):
        print 'Processing the forum page......'
        self.forum_url = forum_url
        try:
            br.open(self.forum_url)
        except:
            return False
        response = br.response()
        html = response.read().replace('&#58;',':').replace('.bayw.org','.com')         #for  bayw.org ( reps imdb.com links as imdb.baw.org )and some sites where :  is rep by &#58;
        pattern = re.compile('imdb.com/title/tt\d{7}')
        search = re.search(pattern, html)
        if search:
            imdb_url = search.group()
            movie = new_movie(imdb_url)
            if not movie:
                print 'Sorry, Could not process your request.\n'
                return None
            update_session(request, movie, message = "Processing Forum page")
            self.movie = movie
            self.our_rating = 0
            self.download_links = ''
            try:
                self.save()
            except:
                return None
            return self
        else:
            print 'Sorry, Could not process your request.\n'
            return False
    def fetch_download_links (self,request = None):
        print 'Fetching the download links now......'
        i = 0
        br.open('http://wgtools.com/link-checker/?url=%s' %(self.forum_url))
        response = br.response()
        html = unicode(response.read())
        soup = BeautifulSoup(html)
        links_table = soup.find('table', {'class':'linkstable'})
        result =  links_table.findAll('a',{'style':'color: #368a30; text-decoration: none;'})
        unknown = links_table.findAll('a',{'style':'color: #d5b11f; text-decoration: none;'})   #The results which are marked unknown at wgtools are scrapped here
        if not self.download_links:
            self.download_links = ''
        for a in result:
            link = '%s' %(a['href'])
            if link in self.download_links :        #To check if the link is not already added 
                pass                                #to the movie from any other forum
            else:
                self.download_links += link+'\n'
                i += 1
                print '%d. %s' %(i, a['href'])
        for a in unknown:                           
            link = '%s' %(a['href'])
            if link in self.download_links :        #To check if the link is not already added 
                pass                                #to the movie from any other forum
            else:
                self.download_links += link+'\n'
                i += 1
                print '%d. %s ( Not sure about this link )' %(i, a['href'])
        self.save()
        print '%d new link(s) found\n' %(i)
        return i
    def download_links_for_html(self):
        return self.download_links.replace('\n', '<br />')
           
def add_download_info(forum_url, request = None):
    print 'Forum Page:', forum_url
    try:
        down_info = DownloadInfo.objects.get(forum_url = forum_url)
        print 'Info from this forum already in database, will look for new links......'
        update_session(request, down_info.movie, message = 'Already in the database.')
        try:
            if down_info.fetch_download_links() == 0:
                update_session(request, down_info.movie, message = 'No new info found.')   
                return False
            else:
                return down_info
        except :
            print '0 new link(s) found\n'
            return False
    except DownloadInfo.DoesNotExist:
        down_info = DownloadInfo()
        down_info = down_info.process_forum_page(forum_url, request = request)
        if down_info:
            update_session(request, down_info.movie)
            try:
                down_info.fetch_download_links()    
                return down_info
            except :
                print '0 new link(s) found\n'
                return False
        else:
            return None

def manual_add_download_info(imdb_url, forum_url = '', request = None):
    print '\nImdb Info:', imdb_url, '\nForum Page:', forum_url
    try:
        down_info = DownloadInfo.objects.get(forum_url = forum_url)
        print 'Info from this forum already in database, will look for new links......'
        update_session(request, down_info.movie, message = 'Already in the database.')
        try:
            if down_info.fetch_download_links() == 0:
                update_session(request, down_info.movie, message = 'No new info found.')   
                return False
            else:
                return down_info
        except :
            print '0 new link(s) found\n'
            return False
    except DownloadInfo.DoesNotExist:
        'Adding movie'
        movie = new_movie(imdb_url)
        if movie:
            movie.save()
        update_session(request, movie)
        print forum_url
        if forum_url:
            print 'Fetching forum info'
            down_info = DownloadInfo(forum_url = forum_url)
            down_info.movie = movie
            down_info.our_rating = 0
            down_info.fetch_download_links()
            return down_info
        
def add_page(forum_page_url = None, forum_movie_regex = None, request = None):
    if not forum_page_url:
        print 'No Forum Url Supplied'
        return False
        forum_page_url = raw_input('Enter the page where movies are listed :')
    if not (forum_movie_regex and forum_movie_regex.endswith('$')):
        print 'No Movie Regex Supplied'
        return False
        forum_movie_regex = raw_input('Enter the generalized regex for the movie forum links :')
    print 'Will now fetch the movies and their infos, It may take some time......\n'
    try:    
        response =  br.open(forum_page_url)
    except:
        print "Sorry could not open the forum page.\n"
        return None
    forum_links = []
    for forum_Link in br.links(url_regex=forum_movie_regex):
        if not ("Go to last post[IMG]") in forum_Link.text:
            #print forum_Link
            forum_links.append(forum_Link.url)
    dwn_infos = []
    for forum_link in forum_links:
            dwn_info = add_download_info(forum_link, request = request)
            if dwn_info:
                dwn_infos.append(dwn_info)
    print '\n'+str(len(dwn_infos)), 'Movie Download Info added' 
    if dwn_infos:
        return dwn_infos
    else:
        print '\nNo movie found on the page.'
        return False
