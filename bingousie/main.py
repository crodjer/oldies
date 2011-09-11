from google.appengine.ext import db
from waplib import pages
from random import shuffle
from django.utils import simplejson
import datetime
all_numbers = range(1,91)

class GameBoard(db.Model):
    numbers = db.ListProperty(int, default=all_numbers)
    index = db.IntegerProperty(int, default = 0)
    finished = db.BooleanProperty(default = False)
    last_update = db.DateTimeProperty(auto_now=True)
    def increment_index(self):
        if not self.finished:
            if self.index<89:
                self.index+=1
                if self.index==89:
                    self.finished = True
                self.save()

        return self.numbers[self.index]

    def passed_numbers(self):
        return self.numbers[:self.index]
    def current_number(self):
        return self.numbers[self.index]

    def passed_numbers_json(self):
        return simplejson.dumps(self.passed_numbers())

class MainPage(pages.BasePage):
    def DoGet(self):
        self.render_template('index.html')

class TableGen(pages.BasePage):
    def DoGet(self):
        self.render_template('table_gen.html', { 'all_numbers': all_numbers })

class GamePage(pages.BasePage):
    def DoGet(self, id):
        gameboard = GameBoard.get_by_id(int(id))
        self.render_template('game.html', { 'board':gameboard })

class GenNumber(pages.BasePage):
    def DoGet(self, id):
        gameboard = GameBoard.get_by_id(int(id))
        gameboard.increment_index()
        self.redirect("/%d/" %(gameboard.key().id()))

class GenNumberAJAX(pages.BasePage):
    def DoGet(self, id):
        gameboard = GameBoard.get_by_id(int(id))
        self.response.out.write(simplejson.dumps([gameboard.increment_index(), gameboard.finished]))

class NewGame(pages.BasePage):
    def DoGet(self):
        gameboard = GameBoard()
        shuffle(gameboard.numbers)
        gameboard.save()
        self.redirect("/%d/" %(gameboard.key().id()) )

class CleanUp(pages.BasePage):
    def DoGet(self):
        max_time = datetime.datetime.now() - datetime.timedelta(days = 10)
        gameboards = db.Query(GameBoard).filter("last_update < ", max_time)
        for board in gameboards:
            board.delete()

class LoginPage(pages.BasePage):
    def DoGet(self):
        self.render_template('login.html')

