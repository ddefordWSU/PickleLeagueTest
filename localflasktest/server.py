from flask import Flask, render_template, request, redirect, url_for
import csv
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open('data/roster_test.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        roster = []
        for row in data:
            roster.append({
              "id": row[0],
              "name": row[1]
            })
    return render_template("index.html", roster=roster)

#def hello():
#  return render_template("index.html")

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        with open('data/roster_test.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            roster = []
            for row in data:
                roster.append({
                "id": row[0],
                "name": row[1]
                })
                
        userdata = dict(request.form)
        newname = userdata["fname"] +" " + userdata["lname"][0] +"."
        newid = str(len(roster) + 1)
        
    with open('data/roster_test.csv',  newline="\n", mode='a') as csv_file:
        data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data.writerow([newid, newname])
    return f"You have been added to the roster!"# \n Return to main webapge: {url_for('index')}"


@app.route("/submit2", methods=["GET", "POST"])
def submit2():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        with open("./data/matches_test.csv",'r') as f:
            reader = csv.reader(f)
            matches = list(reader)

                
        userdata = dict(request.form)
        
    with open('data/matches_test.csv',  newline="\n", mode='a') as csv_file:
        data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data.writerow([len(matches),userdata["p1"],userdata["p2"],userdata["s1"],userdata["p3"],userdata["p4"],userdata["s2"]])
    return f"Your match has been recorded as match ID #: {len(matches)}"# \n Return to main webpage: {url_for('index')}"

   
if __name__ == "__main__":
  app.run()
