from app import app, db



""" With a regular interpreter session, the app symbol is not known unless it is explicitly imported, butwhen using flask shell, the command pre-imports the application instance. The nice thing about flaskshell is not that it pre-imports app, but that you can configure a "shell context", which is a list ofother symbols to pre-import.

The following function in microblog.py creates a shell context that adds the database instance and models to the shell session: """

from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}