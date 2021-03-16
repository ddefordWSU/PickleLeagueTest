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
    return render_template("submit.html")#f"You have been added to the roster!"# \n Return to main webapge: {url_for('index')}"


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
    return  render_template("submit.html")#f"Your match has been recorded as match ID #: {len(matches)}"# \n Return to main webpage: {url_for('index')}"

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
        tlist = []
        for x in roster.keys():
            if g_dict[int(x)] > 0:
                tlist.append([roster[x],x,w_dict[int(x)],p_dict[int(x)],g_dict[int(x)]])
        
        tlist.sort(key=lambda x:(x[2],x[3]))
        tlist.reverse()
        for t in tlist:
            plist.append({"name":t[0],"id":t[1],"wins":t[2],"points":t[3],"games":t[4]})
                              
        return render_template("statsI.html", plist=plist)                          

@app.route("/submitT", methods=["GET", "POST"])
def submitT():
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

        teamlist = []
        tlist = []
        for x in roster.keys():
            for y in roster.keys():
                if g_dict_p[(int(x),int(y))] > 0:
                    tlist.append([(roster[x],roster[y]),(x,y),w_dict_p[(int(x),int(y))],p_dict_p[(int(x),int(y))],g_dict_p[(int(x),int(y))]])
        
        tlist.sort(key=lambda x:(x[2],x[3]))
        tlist.reverse()
        for t in tlist:
            teamlist.append({"name":t[0],"id":t[1],"wins":t[2],"points":t[3],"games":t[4]})
                              
        return render_template("statsT.html", teamlist=teamlist)                          

@app.route("/submitH", methods=["GET", "POST"])
def submitH():
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
        
        
        userdata = dict(request.form)


        h2h_g = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}
        h2h_w = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}
        h2h_p = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}

        for game in matches:

            game = [int(x) for x in game]

            game = [game[0],(game[1],game[2],game[3]),(game[4],game[5],game[6])]

            for i in range(2):
                h2h_g[(game[1][0],game[2][0])] += 1
                h2h_g[(game[1][0],game[2][1])] += 1
                h2h_g[(game[1][1],game[2][0])] += 1
                h2h_g[(game[1][1],game[2][1])] += 1
                h2h_g[(game[2][0],game[1][0])] += 1
                h2h_g[(game[2][0],game[1][1])] += 1
                h2h_g[(game[2][1],game[1][0])] += 1
                h2h_g[(game[2][1],game[1][1])] += 1

                h2h_p[(game[1][0],game[2][0])] += game[1][2]
                h2h_p[(game[1][0],game[2][1])] += game[1][2]
                h2h_p[(game[1][1],game[2][0])] += game[1][2]
                h2h_p[(game[1][1],game[2][1])] += game[1][2]
                h2h_p[(game[2][0],game[1][0])] += game[2][2]
                h2h_p[(game[2][0],game[1][1])] += game[2][2]
                h2h_p[(game[2][1],game[1][0])] += game[2][2]
                h2h_p[(game[2][1],game[1][1])] += game[2][2]

                if game[1][2] == 11:

                    h2h_w[(game[1][0],game[2][0])] += 1
                    h2h_w[(game[1][0],game[2][1])] += 1
                    h2h_w[(game[1][1],game[2][0])] += 1
                    h2h_w[(game[1][1],game[2][1])] += 1
                else:
                    h2h_w[(game[2][0],game[1][0])] += 1
                    h2h_w[(game[2][0],game[1][1])] += 1
                    h2h_w[(game[2][1],game[1][0])] += 1
                    h2h_w[(game[2][1],game[1][1])] += 1
                    
        Hlist = []
        tlist = []
        
        x = userdata["player1"][0]
        y = userdata["player2"][0]
        
        tlist.append([(roster[x],roster[y]),(x,y),h2h_w[(int(x),int(y))],h2h_p[(int(x),int(y))],h2h_g[(int(x),int(y))]])
        
        #tlist.sort(key=lambda x:(x[2],x[3]))
        #tlist.reverse()
        for t in tlist:
            Hlist.append({"name":t[0],"id":t[1],"wins":t[2],"points":t[3],"games":t[4]})
                              
        return render_template("statsH2H.html", Hlist=Hlist)                          

@app.route("/submitP", methods=["GET", "POST"])
def submitP():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        if userdata['League'] == "LINT":
            session["name"] = "Lewiston Intermediate League"
            session["suff"] = "LINT"
            if userdata['pwd'] == "LINTPASS":
                with open('data/roster_LINT.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1]
                        })
                return render_template("home.html", roster=roster)
            else:
                return render_template("wrongPass.html")
            
        if userdata['League'] == "LADV":
            session["name"] = "Lewiston Advanced League"
            session["suff"] = "LADV"
            if userdata['pwd'] == "LADVPASS":
                with open('data/roster_LADV.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1]
                        })
                return render_template("home.html", roster=roster)
            else:
                return render_template("wrongPass.html")           

        if userdata['League'] == "PP":
            session["name"] = "Pullman Public League"
            session["suff"] = "PP"
            if userdata['pwd'] == "PPPASS":
                with open('data/roster_PP.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1]
                        })
                return render_template("home.html", roster=roster)
            else:
                return render_template("wrongPass.html")               

        if userdata['League'] == "T":
            session["name"] = "Test League"
            session["suff"] = "test"
            if userdata['pwd'] == "test":
                with open('data/roster_test.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1]
                        })
                return render_template("home.html", roster=roster)
            else:
                return render_template("wrongPass.html")


            
            
            
if __name__ == "__main__":
  app.run()
