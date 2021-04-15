from datetime import datetime

from peewee import MySQLDatabase, Model, CharField, ForeignKeyField, \
    DateField, DateTimeField, SmallIntegerField, TextField

from playhouse.db_url import connect

# db = MySQLDatabase('goodreads2', user='goodreads', password='goodreads',
#                    host='localhost', port=3306)
database = connect('mysql://goodreads:goodreads@localhost/goodreads2')


class BaseModel(Model):
    class Meta:
        database = database

    def __str__(self):
        return str(self.id)


class User(BaseModel):
    username = CharField(max_length=32)
    password = CharField(max_length=32)

    @classmethod
    def authenticate(cls, username, password):
        return cls.select().where(
            cls.username == username, cls.password == password
        ).first()


class Book(BaseModel):
    isbn = CharField(max_length=32)
    name = CharField(max_length=255)


class Author(BaseModel):
    name = CharField(max_length=32)


class Shelf(BaseModel):
    READ = 'read'
    CURENTLY_READ = 'currently read'
    WANT_TO_READ = 'want to read'
    name = CharField(max_length=32)
    user = ForeignKeyField(User, backref='shelves')


class BookShelf(BaseModel):
    user = ForeignKeyField(User, backref='book_shelves')
    book = ForeignKeyField(Book, backref='book_shelves')
    shelf = ForeignKeyField(Shelf, backref='book_shelves')
    start_date = DateField(null=True)
    end_date = DateField(null=True)
    rate = SmallIntegerField()
    comment = TextField()

    created_time = DateTimeField(default=datetime.now())
    
    def change_to_read(self):
        read_shelf = self.user.shelves.where(Shelf.name == Shelf.READ)
        self.shelf = read_shelf
        self.save()

class BookAuthor(BaseModel):
    book = ForeignKeyField(Book, backref='authors')
    author = ForeignKeyField(Author, backref='books')


class BookTranslator(BaseModel):
    book = ForeignKeyField(Book, backref='translators')
    translators = ForeignKeyField(Author, backref='translated_books')


class UserAuthorRelation(BaseModel):
    user = ForeignKeyField(User, backref='followed_authors')
    author = ForeignKeyField(Author, backref='following_users')


class UserRelation(BaseModel):
    following = ForeignKeyField(User, backref='following')
    follower = ForeignKeyField(Author, backref='follower')
