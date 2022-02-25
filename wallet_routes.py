from application import app


@app.route('/wallet')
def wallet():
    return "Hello Wallet"
