from flask import Flask
from flask_admin import Admin

import peewee
from flask_admin.contrib.peewee import ModelView

from flask_restful import Resource, Api

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
api = Api(app)

db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)

class BaesModel(peewee.Model):
    class Meta:
        database = db

class User(BaesModel):
    username = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)

    def __unicode__(self):
        return self.username

class UserInfo(BaesModel):
    key = peewee.CharField(max_length=64)
    value = peewee.CharField(max_length=64)

    user = peewee.ForeignKeyField(User)

    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)

class Post(BaesModel):
    title = peewee.CharField(max_length=120)
    text = peewee.TextField(null=False)
    date = peewee.DateTimeField()

    user = peewee.ForeignKeyField(User)

    def __unicode__(self):
        return self.title

class UserAdmin(ModelView):
    inline_models = (UserInfo,)

class PostAdmin(ModelView):
    column_exclude_list = ['text']
    column_sortable_list = ('title', ('user', User.email), 'date')
    column_searchable_list = ('title', User.username)
    column_filters = ('title', 'date', User.username)
    form_ajax_refs = {
            'user': {
                'fields': (User.username, 'email')
            }
    }

@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    admin = Admin(app, name='microblog', template_mode='bootstrap3')

    admin.add_view(UserAdmin(User))
    admin.add_view(PostAdmin(Post))

    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
    except:
        pass

    app.run(debug=True)
