import sqlite3 as sql
from flask import Flask, render_template, request, redirect,url_for

app = Flask(__name__, template_folder="templates")

global name

con = sql.connect('game.db')
cur = con.cursor()
#cur.execute("INSERT INTO scene VALUES(?,?,?,?,?)", ("toilet", "turn_light_on, go_inside, bed","toilet.png",0,"toilet.html"))
a = cur.execute('''SELECT * FROM scene''').fetchall()
print(a)
con.commit()

@app.route("/")
def start():
    con = sql.connect('game.db')
    cur = con.cursor()
    print("working")
    scene = cur.execute('''SELECT scene FROM users WHERE name = ?''', (request.remote_addr,)).fetchone()[0]
    html = cur.execute('''SELECT html FROM scene WHERE name = ?''', (scene,)).fetchone()[0]
    print(scene, html)
    if request.remote_addr not in cur.execute('''SELECT * FROM users''').fetchall():
        try:
            cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", (request.remote_addr,request.remote_addr,0, 'house',))
        except sql.IntegrityError:
            pass

    a = cur.execute('''SELECT * from users WHERE ip = ?''', (str(request.remote_addr), )).fetchall()[0]
    con.commit()
    return render_template(html, name=a[1])

@app.route("/", methods=["POST"])
def start_post():
    con = sql.connect('game.db')
    cur = con.cursor()
    scene = request.form.to_dict()['name']
    print(scene, '??????')
    html = cur.execute('''SELECT html FROM scene WHERE name = ?''', (scene,)).fetchone()[0]

    return render_template(html)




if __name__ == "__main__":
    app.run(host="172.20.10.3")