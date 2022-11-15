from app import app, db
from models import Post

app.app_context().push()
db.create_all()
p = Post('Hello!')
db.session.add(p)
db.session.commit()
posts = Post.query.all()
