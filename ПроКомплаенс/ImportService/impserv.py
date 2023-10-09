from app import app, db, cli


@app.shell_context_processor
def make_shell_context():
    return {'db': db}

app.run()