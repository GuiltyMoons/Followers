from flask import render_template, url_for, flash, redirect, request, abort
import sys
from followers import app, db
from followers import getFollow
from followers import insta
from followers.models import Account, History, Settings
from datetime import datetime




@app.route('/update_theme', methods=['POST'])
def updateTheme():
    settings = Settings.query.first()
    settings.color_scheme = request.form.get('theme')
    db.session.commit()
    return redirect(url_for('settings'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/privacy-policy')
def dataPrivacyPolicy():
    theme = Settings.query.first().color_scheme
    return render_template('DataPrivacyPolicy.html', title="Data Privacy Policy", theme=theme)



#STILL NEEDS TO BE FINISHED
@app.route('/getData', methods=['POST'])#Get data from the NODE JS Puppeteer
def getData():
    username = request.json.get('username')
    followers = request.json.get('followers')
    following = request.json.get('following')
    profile_pic_url = request.json.get('profilePicURL')
    output = f"{username}\nFollowers:{followers}\nFollowing:{following}\nProfile Pic URL: {profile_pic_url}"
    print(f"{username}\nFollowers:{followers}\nFollowing:{following}\nProfile Pic URL: {profile_pic_url}", file=sys.stderr)#Logging output

    account = Account.query.filter_by(username=username).first()
    if not account:
        new_account = Account(username=username)
        db.session.add(new_account)
        db.session.commit()
        account = Account.query.filter_by(username=username).first()

    history = History(date=datetime.utcnow(),followers=followers, following=following, owner=account)
    db.session.add(history)
    db.session.commit()


    return output


#STILL NEEDS TO BE FINISHED
@app.route('/recent')
def recent():
    data = []
    accounts = Account.query.all()
    for account in accounts:
        history = (account.history)
        if len(history) > 0:
            print(history[-1], history[-1].owner.username)


    return 'hi'




#REWORK WITH PUPPETEER
@app.route('/update')
def update():
    #accounts = Account.query.all()
    #for account in accounts:
    #    data = loop.run_until_complete(ig.getData(account.username))
    #    db.session.add(History(date=datetime.utcnow(),followers=data[0], following=data[1], owner = account))
    #    db.session.commit()
    #flash("History updated!", "success")
    return redirect(request.referrer)



#REWORK WITH PUPPETEER
@app.route('/')
@app.route('/home')
def index():
    theme = Settings.query.first().color_scheme
    accounts = []
    sql_accounts = Account.query.all()
    for account in sql_accounts:
        #data = loop.run_until_complete(ig.getData(account.username))
        data = account.username
        accounts.append((account.username, data))


    return render_template('index.html',title="index",username="ErickMeyer", accounts=accounts, theme=theme)

@app.route('/settings')
def settings():
    theme = Settings.query.first().color_scheme
    return render_template('settings.html', title='settings',theme=theme)

@app.route('/analytics')
def default_analytics():
    account = Account.query.first()
    if account == None:
        flash("ERROR! YOU have to add an account to use analytics", "error")
        return redirect(url_for('index'))
    return redirect(url_for('analytics', username=account.username))

@app.route('/analytics/<username>')
def analytics(username):
    theme = Settings.query.first().color_scheme
    account = Account.query.filter_by(username=username).first()
    accounts = Account.query.all()
    if not account:
        flash("{} does not exist".format(username), "error")
        return redirect(url_for('index'))
    history = account.history
    historical_data = {}

    for h in history:
        historical_data[str(h.date)] = (h.followers, h.following)

    return render_template('analytics.html', title='analytics', history=historical_data, account=account, accounts=accounts,theme=theme)



#REWORK WITH PUPPETEER
@app.route('/search/<username>', methods = ['POST', 'GET'])
def search(username):
    #data = loop.run_until_complete(ig.getData(username))
    #return render_template('search.html', title='search', username=username.lower(), data=data)
    return "TODO"

@app.route('/add/<username>', methods = ['POST', 'GET'])
def add(username):
    account = Account.query.filter_by(username=username).first()
    if account:
        flash("That account is already being checked!", "error")
        return redirect(url_for("index"))
    else:
        account = Account(username=username)
        db.session.add(account)
        db.session.commit()
        flash("Account added successfully!", "success")
        return redirect(url_for("index"))


@app.route('/delete/<username>')
def delete(username):
    account = Account.query.filter_by(username=username).first()
    if account:
        history_list = account.history
        for history in history_list:
            db.session.delete(history)
        db.session.delete(account)
        db.session.commit()
        flash("{} deleted!".format(username), "success")
        return redirect(url_for("index"))
    else:
        flash("Error Deleting User!", "error")
        return redirect(url_for("index"))



#REWORK WITH PUPPETEER
#may not even need any of this anymore
#@app.route('/quit')
#def quit():
#    loop.run_until_complete(ig.close())
#    loop.close()
#    return "quitting"
