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

@app.route("/submitI", methods=["GET", "POST"])
def submitI():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        with open("./data/matches_test.csv",'r') as f:
            reader = csv.reader(f)
            matches = list(reader)
            
        with open('data/roster_test.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            roster = {}
            for row in data:
                roster[row[0]] = row[1]

        g_dict = {int(x):0 for x in roster.keys()}
        w_dict = {int(x):0 for x in roster.keys()}
        p_dict = {int(x):0 for x in roster.keys()}

        g_dict_p = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}
        w_dict_p = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}
        p_dict_p = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}

        for game in matches:

            game = [int(x) for x in game]

            game = [game[0],(game[1],game[2],game[3]),(game[4],game[5],game[6])]

            for i in range(2):
                pair = game[i+1]
                g_dict[pair[0]] +=1
                g_dict_p[(pair[0],pair[1])] +=1
                g_dict_p[(pair[1],pair[0])] +=1

                if pair[2] ==11:
                    w_dict[pair[0]] +=1
                    w_dict_p[(pair[0],pair[1])] +=1
                    p_dict[pair[0]] +=11
                    p_dict_p[(pair[0],pair[1])] +=11
                else:
                    p_dict[pair[0]] += pair[2]
                    p_dict_p[(pair[0],pair[1])] +=pair[2]

        plist = []
        for x in roster.keys():
            if g_dict[int(x)] > 0:
                plist.append({"name":roster[x],"id":x,"wins":w_dict[int(x)],"points":p_dict[int(x)],"games":g_dict[int(x)]})
                              
        return render_template("statsI.html", plist=plist)                          

if __name__ == "__main__":
  app.run()
