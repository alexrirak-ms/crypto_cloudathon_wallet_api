from application import app

@app.route('/transaction')
def transaction():
    return "Hello Transaction"
