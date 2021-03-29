from flask import Flask, render_template, request, redirect, url_for, session
#from flask_session import Session
import csv
import json
import logging

app = Flask(__name__)
#SESSION_TYPE = 'redis'
#app.config.from_object(__name__)
#Session(app)
app.secret_key = "1769"

@app.before_request
def log_the_request():
    logger.info(request.remote_addr)
    logger.info(request)
    
    
@app.route("/")
def index():
    with open('data/roster_test.csv') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        roster = []
        for row in data:
            roster.append({
              "id": row[0],
              "name": row[1],
              "city": row[2],
              "contact": row[3]            
            })
    return render_template("index.html", roster=roster)

@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        suff = session.get("suff")
        
        with open(f'data/roster_{suff}.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            roster = []
            roster_keys = []
            for row in data:
                roster.append({
                "id": row[0],
                "name": row[1]
                })
                roster_keys.append(row[1])
                
        
        #print(roster_keys)      
        userdata = dict(request.form)
        for k in list(userdata.keys()):
            logger.info(str(suff)+" "+str(k)+" "+str(userdata[k]))
        
        newname = userdata["fname"] +" " + userdata["lname"][0] +"."
        #print(newname)
        newid = str(len(roster) + 1)
        
        if newname in roster_keys:
            return render_template("doubleplayer.html")
            
        
    with open(f'data/roster_{suff}.csv',  newline="\n", mode='a') as csv_file:
        data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data.writerow([newid, newname, userdata["city"],userdata["contact"]])
    return render_template("submit.html")#f"You have been added to the roster!"# \n Return to main webapge: {url_for('index')}"


@app.route("/submit2", methods=["GET", "POST"])
def submit2():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        suff = session.get("suff")
        with open(f"./data/matches_{suff}.csv",'r') as f:
            reader = csv.reader(f)
            matches = list(reader)

            
                
        userdata = dict(request.form)
        for k in list(userdata.keys()):
            logger.info(str(suff)+" "+str(k)+" "+str(userdata[k]))
        plist= list(set([userdata["p1"],userdata["p2"],userdata["p3"],userdata["p4"]]))
        if len(plist)  < 4:
            return render_template("fourplayer.html")
            
            
        with open(f'data/roster_{suff}.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            roster = []
            roster_keys = []
            for row in data:
                roster_keys.append(row[0])
                roster.append({
                "id": row[0],
                })   
        
        #print(roster_keys)
        for person in plist:
            if person not in roster_keys:
                return render_template("noplayer.html")
                
    
        if 11 not in [int(userdata["s1"]),int(userdata["s2"])]:
            return render_template("no11.html")

        #if len(matches) == 0:
        #     with open(f'data/matches_{suff}.csv',  newline="\n") as csv_file:
        #        data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #        data.writerow([len(matches),userdata["p1"],userdata["p2"],userdata["s1"],userdata["p3"],userdata["p4"],userdata["s2"]])
        #     return  render_template("submit.html")#f"Your match has been recorded as match ID #: {len(matches)}"# \n Return to main webpage: {url_for('index')}"
        
        
    with open(f'data/matches_{suff}.csv',  newline="\n", mode='a') as csv_file:
        data = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data.writerow([len(matches),userdata["p1"],userdata["p2"],userdata["s1"],userdata["p3"],userdata["p4"],userdata["s2"]])
    return  render_template("submit.html")#f"Your match has been recorded as match ID #: {len(matches)}"# \n Return to main webpage: {url_for('index')}"

@app.route("/submitI", methods=["GET", "POST"])
def submitI():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        
        suff = session.get("suff")
        
        with open(f"./data/matches_{suff}.csv",'r') as f:
            reader = csv.reader(f)
            matches = list(reader)
            
        if len(matches) == 0:
            return render_template("nomatches.html")
        if len(matches) == 1:
            if len(matches[0])==0:
                return render_template("nomatches.html")           
        with open(f'data/roster_{suff}.csv') as csv_file:
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
        
        if len(matches[0]) < 6:
            matches.pop(0)

        for game in matches:

            game = [int(x) for x in game]
            
            #print(matches)
            #print(game)

            game = [game[0],(game[1],game[2],game[3]),(game[4],game[5],game[6])]

            for i in range(2):
                pair = game[i+1]
                g_dict[pair[0]] +=1
                g_dict[pair[1]] +=1
                g_dict_p[(pair[0],pair[1])] +=1
                g_dict_p[(pair[1],pair[0])] +=1

                if pair[2] ==11:
                    w_dict[pair[0]] +=1
                    w_dict[pair[1]] +=1
                    w_dict_p[(pair[0],pair[1])] +=1
                    p_dict[pair[0]] +=11
                    p_dict[pair[1]] +=11
                    p_dict_p[(pair[0],pair[1])] +=11
                else:
                    p_dict[pair[0]] += pair[2]
                    p_dict[pair[1]] += pair[2]
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
        suff = session.get("suff")
   
        with open(f"./data/matches_{suff}.csv",'r') as f:
            reader = csv.reader(f)
            matches = list(reader)
            
        if len(matches) == 0:
            return render_template("nomatches.html")
        if len(matches) == 1:
            if len(matches[0])==0:
                return render_template("nomatches.html")           
            
        with open(f'data/roster_{suff}.csv') as csv_file:
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
        
        if len(matches[0]) < 6:
            matches.pop(0)

        

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
                if int(x) < int(y):
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
        suff = session.get("suff")
        
        with open(f"./data/matches_{suff}.csv",'r') as f:
            reader = csv.reader(f)
            matches = list(reader)
            
        if len(matches) == 0:
            return render_template("nomatches.html")
        if len(matches) == 1:
            if len(matches[0])==0:
                return render_template("nomatches.html")           
            
        with open(f'data/roster_{suff}.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            roster = {}
            for row in data:
                roster[row[0]] = row[1]
        
        
        userdata = dict(request.form)


        h2h_g = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}
        h2h_w = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}
        h2h_p = {(int(x),int(y)):0 for x in roster.keys() for y in roster.keys()}

        if len(matches[0]) < 6:
            matches.pop(0)

    
        
        for game in matches:

            game = [int(x) for x in game]

            game = [game[0],(game[1],game[2],game[3]),(game[4],game[5],game[6])]

            for i in range(1):
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
        
        if h2h_g[(int(x),int(y))] == 0:
            return render_template("NoHead.html")
        
        tlist.append([(roster[x],'vs',roster[y]),(x,'vs',y),h2h_w[(int(x),int(y))],h2h_p[(int(x),int(y))],h2h_p[(int(y),int(x))],h2h_g[(int(x),int(y))]])
        
        #tlist.sort(key=lambda x:(x[2],x[3]))
        #tlist.reverse()
        for t in tlist:
            Hlist.append({"name":t[0],"id":t[1],"wins":t[2],"points":t[3],"pointsagainst":t[4],"games":t[5]})
                              
        return render_template("statsH2H.html", Hlist=Hlist)                          

@app.route("/submitP", methods=["GET", "POST"])
def submitP():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        userdata = dict(request.form)

        if userdata['pwd'] == "test":
            session["name"] = "Test League"
            session["suff"] = "test"
            sess ={"name":"Test League"}
            if userdata['pwd'] == "test":
                with open('data/roster_test.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1],
                          "city": row[2],
                          "contact": row[3]            
                        })
                return render_template("home.html", roster=roster,sess=sess)
            else:
                return render_template("wrongPass.html")
        
        
        try:
            temp = userdata['League']
        except KeyError:
            return render_template("noLeague.html")
        #if not userdata['League']:
        #    return render_template("noLeague.html")
            
        
        if userdata['League'] == "LINT":
            session["name"] = "Lewiston Intermediate League"
            session["suff"] = "LINT"
            sess ={"name":"Lewiston Intermediate League"}
            if userdata['pwd'] == "LINTPASS":
                with open('data/roster_LINT.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1],
                          "city": row[2],
                          "contact": row[3]            
                        })
                return render_template("home.html", roster=roster,sess=sess)
            else:
                return render_template("wrongPass.html")
            
        if userdata['League'] == "LADV":
            session["name"] = "Lewiston Advanced League"
            session["suff"] = "LADV"
            sess ={"name":"Lewiston Advanced League"}
            if userdata['pwd'] == "LADVPASS":
                with open('data/roster_LADV.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1],
                          "city": row[2],
                          "contact": row[3]            
                        })
                return render_template("home.html", roster=roster,sess=sess)
            else:
                return render_template("wrongPass.html")           

        if userdata['League'] == "PP":
            session["name"] = "Pullman Public League"
            session["suff"] = "PP"
            sess ={"name":"Pullman Public League"}
            if userdata['pwd'] == "PPPASS":
                with open('data/roster_PP.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1],
                          "city": row[2],
                          "contact": row[3]            
                        })
                    return render_template("home.html", roster=roster,sess=sess)
            else:
                return render_template("wrongPass.html")               

        if userdata['League'] == "PT":
            session["name"] = "Pullman 4.0+ Tournament"
            session["suff"] = "PT"
            sess ={"name":"Pullman 4.0+ Tournament"}
            if userdata['pwd'] == "PTPASS":
                with open('data/roster_PT.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1],
                          "city": row[2],
                          "contact": row[3]            
                        })
                    return render_template("home.html", roster=roster,sess=sess)
            else:
                return render_template("wrongPass.html")               
            
        if userdata['League'] == "T":
            session["name"] = "Test League"
            session["suff"] = "test"
            sess ={"name":"Test League"}
            if userdata['pwd'] == "test":
                with open('data/roster_test.csv') as csv_file:
                    data = csv.reader(csv_file, delimiter=',')
                    roster = []
                    for row in data:
                        roster.append({
                          "id": row[0],
                          "name": row[1],
                          "city": row[2],
                          "contact": row[3]            
                        })
                return render_template("home.html", roster=roster,sess=sess)
            else:
                return render_template("wrongPass.html")


@app.route("/submitR", methods=["GET", "POST"])
def submitR():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        #userdata = dict(request.form)
        sess = {"name":session.get("name")}
        return render_template("register.html", sess=sess)
                    
@app.route("/submitM", methods=["GET", "POST"])
def submitM():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        sess = {"name":session.get("name")}
        suff = session.get("suff")
        
        with open(f'data/roster_{suff}.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            roster = []
            for row in data:
                roster.append({
                  "id": row[0],
                  "name": row[1],
                  "city": row[2],
                  "contact": row[3]            
                })
        #userdata = dict(request.form)
        sess = {"name":session.get("name")}
        return render_template("enter.html", roster=roster, sess=sess)
 
                        
@app.route("/submitS", methods=["GET", "POST"])
def submitS():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        #userdata = dict(request.form)
        sess = {"name":session.get("name")}
        return render_template("standings.html", sess=sess)

@app.route("/submitRR", methods=["GET", "POST"])
def submitRR():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        userdata = dict(request.form)
        n = userdata['numplay']
        
        if n < 4 or n > 24:
            return render_template("RRwrong.html")
        
        

	    url = f"http://math.wsu.edu/faculty/ddeford/PB_Brackets/pb{n}.json"
	    r = requests.get(url)
	    wdict = r.json()
        
        courts = math.floor(n/4)
        byes = n%4

        rows = [['Court ' + str(x+1) for x in range(courts)]]
        if byes > 0: 
            rows[0].append('Bye(s)')
        rows[0].insert(0,'Round')

        for i in range(len(wdict[str(n)])):
            rows.append([])
            row = wdict[str(n)][i]
            for j in range(courts):
                #print(courts)
                #print(row)

                rows[-1].append(names[row[j][0][0]] + '/' + names[row[j][0][1]] + " vs. " + names[row[j][1][0]] + '/' + names[row[j][1][1]])
                #print(rows)
            if byes >0: 
                rows[-1].append(names[row[-1][0]])

                for k in range(1,byes):
                    rows[-1][-1] = rows[-1][-1] + " " + (names[row[-1][k]])

            rows[-1].insert(0,str(i+1))
            
            return render_template("RR.html", plist=rows)
    
@app.route("/goHome", methods=["GET", "POST"])
def goHome():
    if request.method == "GET":
        return redirect(url_for('index'))
    elif request.method == "POST":
        #userdata = dict(request.form)
        sess = {"name":session.get("name")}
        suff = session.get("suff")
        
        with open(f'data/roster_{suff}.csv') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            roster = []
            for row in data:
                roster.append({
                  "id": row[0],
                  "name": row[1],
                  "city": row[2],
                  "contact": row[3]            
                })

        
        return render_template("home.html", roster=roster, sess=sess)

                        
if __name__ == "__main__":
    from waitress import serve
    #logging.basicConfig(filename='app.log',level=logging.DEBUG)
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)
    
    handler = logging.FileHandler('app2.log')
    logger.addHandler(handler)
    
    serve(app, host="0.0.0.0", port=8080)
  #app.run()
