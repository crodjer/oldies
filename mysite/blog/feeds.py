from django.contrib.syndication.views import Feed
from blog.models import Post
from django.utils.feedgenerator import Atom1Feed
import markdown

class BlogFeed(Feed):
    feed_type = Atom1Feed
    title = "Rohan Jain's blog"
    link = "/blog/feed/"
    description = "A technical blog by Rohan Jain"

    def items(self):
        return Post.objects.filter(publish=True, is_update=False)

    def item_author_name(self, item):
        return item.user.get_full_name()
    
    def item_title(self, item):
        return item.title    
        
    def item_description(self, item):
        return markdown.markdown(item.content, ['headerid','tables','toc','abbr','fenced_code'])
    
    def item_pubdate(self, item):
        return item.updated_on    
