from function import *
import threading

token = []

apps = {
    "LITE":"ANDROIDLITE\t2.14.0\tAndroid OS\t5.1.1",
    "IOS":"GAK TAU",
    "MAC":"ISI SENDIRI NTOD"
}

admin = ["ue2330fdb6b7db69eb771c3176388d0ff"]
mbing = {}
bots = {
    "cl":0,
    "botsNum":{},
    "botsMid":{},
    "loader":[],
    "teams":{},
    "sdk":["ue2330fdb6b7db69eb771c3176388d0ff"]
}
group = {
    "list":{},
    "qr":[],
    "invite":[],
    "kick":[],
    "cancel":[],
    "join":[]
}
blacklist = []
autoPurge = False

def loginBots():
    for i in range(len(token)):
        tok = token[i]
        app = "MAC"
        if tok.startswith("u"):
            app = "LITE"
        cl = BE_Team(myToken=token[i],myApp=apps[app])
        pf = cl.getProfile()
        mbing[pf.mid] = cl
        bots["botsNum"][pf.mid] = i
        bots["botsMid"][i] = pf.mid
        bots["teams"][pf.mid] = []
        cekGroup(cl, pf.mid)
        checkContact(cl, admin)
        #configSet(cl, pf.mid)

def belekin(enemy):
    if enemy not in blacklist:
        blacklist.append(enemy)

def purge(client, to):
    x = []
    m = list(client.gc(to, "members"))
    for i in m:
        if i in blacklist:
            x.append(i)
    for j in x:
        client.deleteOtherFromChat(to, [j])

def goQR(client, to, act):
    try:
        client.gc(to, "ticket", act)
    except:
        pass

def goKick(to, enemy):
    if len(group["list"][to]["in"]) > 0:
        try:
            mbing[random.choice(group["list"][to]["in"])].deleteOtherFromChat(to, [enemy])
        except:
            pass

def goCancel(to, enemy):
    if len(enemy) > 34:
        x = (len(enemy)//33)
        if len(group["list"][to]["in"]) > 0:
            for i in range(x):
                try:
                    mbing[random.choice(group["list"][to]["in"])].cancelChatInvitation(to, [enemy[i*33:i*33+33]])
                except:
                    pass
    else:
        if len(group["list"][to]["in"]) > 0:
            try:
                mbing[random.choice(group["list"][to]["in"])].cancelChatInvitation(to, [enemy])
            except:
                pass

def checkContact(client, mid):
    fl = client.getAllContactIds()
    if mid not in fl:
        try:
            client.findAndAddContactsByMid(mid)
            time.sleep(5)
        except:
            pass

def peroQR(client, to, enemy, myself):
    if to in group["qr"] or enemy in blacklist:
        if enemy not in bots["sdk"]:
            if len(group["list"][to]["in"]) > 0:
                goQR(mbing[random.choice(group["list"][to]["in"])], to, True)
            goKick(to, enemy)
            belekin(enemy)

def peroInvite(client, to, enemy, victim, myself):
    if to in group["invite"] or enemy in blacklist:
        if enemy not in bots["sdk"]:
            goKick(to, enemy)
            goCancel(ti,victim)
            belekin(enemy)
    else:
        if enemy in bots["sdk"] and myself in victim:
            client.acceptChatInvitation(to)
            apdetGroup(to, myself, "in")
            if autoPurge == True:
                purge(client, to)

def peroCancel(to, enemy, victim, myself):
    if victim == myself and enemy not in group["sdk"]:
        if len(group["list"][to]["in"]) > 0:
            bots["cl"] = bots["botsNum"][random.choice(group["list"][to]["in"])]
        goKick(to, enemy)
        if len(group["list"][to]["out"]) > 0:
            mbing[random.choice(group["list"][to]["in"])].inviteIntoChat(to, group["list"][to]["out"])
        belekin(enemy)
    else:
        if to in group["invite"] or victim in bots["sdk"]:
            if enemy not in bots["sdk"]:
                goKick(to, enemy)
                if victim in bots["botsMid"] and len(group["list"][to]["in"]) > 0 and len(group["list"][to]["out"]) > 0:
                    mbing[random.choice(group["list"][to]["in"])].inviteIntoChat(to, group["list"][to]["out"])
                belekin(enemy)

def peroKick(to, enemy, victim, myself, num):
    if victim == myself and enemy not in bots["sdk"]:
        apdetGroup(to, myself, "out")
        if num == bots["cl"] and len(group["list"][to]["in"]) > 0:
            bots["cl"] = bots["botsNum"][random.choice(group["list"][to]["in"])]
        goKick(to, enemy)
        if len(group["list"][to]["out"]) > 0 and len(group["list"][to]["in"]) > 0:
            mbing[random.choice(group["list"][to]["in"])].inviteIntoChat(to, group["list"][to]["out"])
        belekin(enemy)
    else:
        if to in group["kick"] or victim in bots["sdk"]:
            if enemy not in bots["sdk"]:
                if victim not in bots["botsMid"] and len(group["list"][to]["in"]) > 0:
                    goKick(to, enemy)
                    mbing[random.choice(group["list"][to]["in"])].inviteIntoChat(to, [victim])
                    belekin(enemy)

def peroJoin(to, enemy):
    if to in group["join"] or enemy in blacklist:
        if len(group["list"][to]["in"]) > 0:
            goQR(mbing[random.choice(group["list"][to]["in"])], to, True)
            goKick(to, enemy)
            belekin(enemy)

def cekGroup(client, myself):
    x = client.getAllChatMids().memberChatMids
    for i in x:
        if i not in list(group["list"]):
            group["list"][i] = {
                "in":[myself],
                "out":[]
            }
        elif myself not in group["list"][i]["in"]:
            group["list"][i]["in"].append(myself)

def apdetGroup(to, myself, ops):
    if ops == "in":
        if to not in group["list"].keys():
            group["list"][to] = {
                "in":[myself],
                "out":[]
            }
        else:
            if myself not in group["list"][to]["in"]:
                group["list"][to]["in"].append(myself)
            if myself in group["list"][to]["out"]:
                group["list"][to]["out"].remove(myself)
    elif ops == "out":
        if myself in group["list"][to]["in"]:
            group["list"][to]["in"].remove(myself)
        if myself not in group["list"][to]["out"]:
            group["list"][to]["out"].append(myself)
    elif ops == "ebuset":
        if myself in group["list"][to]["in"]:
            group["list"][to]["in"].remove(myself)
        if myself in group["list"][to]["out"]:
            group["list"][to]["out"].remove(myself)

def worker(op, m):
    try:
        if op.type == 0:
            return

        if op.type == 5:
            #ADD
            mbing[m].findAndAddContactsByMid(op.param1)

        if op.type == 122:
            #QR
            if bots["botsNum"][m] == bots["cl"] and op.param3 == 4:
                peroQR(mbing[m], op.param1, op.param2, m)

        if op.type == 124:
            #Invite
            peroInvite(mbing[m], op.param1, op.param2, op.param3, m)

        if op.type == 128:
            #Leave
            if op.param2 not in bots["sdk"] and bots["botsNum"][m] == bots["cl"]:
                mbing[m].sendMessage(op.param1, "Minggat lo sana")
            else: pass

        if op.type == 130 and bots["botsNum"][m] == bots["cl"]:
            #Join
            peroJoin(op.param1, op.param2)

        if op.type == 133:
            #Kick
            peroKick(op.param1, op.param2, op.param3, bots["botsNum"][m])

        if op.type == 126 and bots["botsNum"][m] == bots["cl"]:
            #Cancel
            peroCancel(op.param1, op.param2, op.param3, m)

        if op.type in [25, 26]:
            #Message
            msg = op.message
            text = str(msg.text)
            msg_id = msg.id
            receiver = msg.to
            msg.from_ = msg._from
            sender = msg._from
            cmd = text
            if msg.toType == 0 and sender != m: to = sender
            else: to = receiver

            if cmd == "ping":
                if sender in admin:
                    mbing[m].sendMessage(to,'BACOD')

            elif cmd == "speed":
                start = time.time()
                mbing[m].sendMessage(to,'Kebotan...')
                total = time.time()-start
                mbing[m].sendMessage(to,str(total))

            elif cmd == "bots" and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    n = "Bot List"
                    for i in range(len(bots["botsMid"])):
                        x = mbing[m].getContact(bots["botsMid"][i]).displayName
                        n += "\n{}. {}".format(i, x)
                    mbing[m].sendMessage(to, n)

            elif cmd == "addbot":
                if sender in admin:
                    for i in bots["botsMid"]:
                        checkContact(mbing[m], i)
                    mbing[m].sendMessage(to, "Done")

            elif cmd == "cek":
                if sender in admin:
                    res = "Normal"
                    try:
                        mbing[m].deleteOtherFromChat(to,[m])
                    except Exception as asu:
                        if 'request blocked':
                            res = "Limit"
                    if res == "Normal" and m not in bots["loader"]:
                        bots["loader"].append(m)
                    mbing[m].sendMessage(to, res)

            elif cmd == "load team":
                if sender in admin:
                    if len(bots["loader"]) > 0:
                        n = 0
                        o = "My team"
                        for i in bots["loader"]:
                            if i != m and i not in bots["teams"][m]:
                                bots["teams"][m].append(i)
                                o += "\n{}. {}".format(n, mbing[m].getContact(i).displayName)
                                n += 1
                    else:
                        o = "Empty"
                    mbing[m].sendMessage(to, o)

            elif cmd == "reset loader" and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    bots["loader"] = []
                    mbing[m].sendMessage(to, "Ahh Ikeh")

            elif cmd.startswith("clientset "):
                if sender in admin:
                    spl = cmd.split(" ")
                    if is_integer(spl[1]):
                        bots["cl"] = int(spl[1])
                    mbing[m].sendMessage(to, "Client set: {}", mbing[m].getContact(bots["botsMid"][int(spl[1])]).displayName)

            elif cmd.startswith("purge ") and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    spl = cmd.split(" ")
                    if spl[1] == "on":
                        autoPurge = True
                    elif spl[1] == "off":
                        autoPurge = False
                    mbing[m].sendMessage(to, "Ah ikehh")

            elif cmd == "oh":
                if sender in admin:
                    mbing[m].deleteSelfFromChat(to)
                    if to in group["list"]:
                        del group["list"]["to"]

            elif cmd == "banlist" and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    if len(blacklist) > 0:
                        mbing[m].sendMessage(to, str(blacklist))

            elif cmd == "clearban" and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    if len(blacklist) > 0:
                        blacklist = []
                        mbing[m].sendMessage(to, "Ahhh ikeh")

            elif cmd == "invteam" and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    if len(bots["teams"][m]) > 0:
                        mbing[m].inviteIntoChat(to, bots["teams"][m])
                        mbing[m].sendMessage(to, "Ahhh ikeh")

            elif cmd == "allin" and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    if len(bots["botsMid"]) > 0:
                        x = []
                        for i in bots["botsMid"]:
                            if m != i:
                                x.append(i)
                        mbing[m].inviteIntoChat(to, i)
                        mbing[m].sendMessage(to, "Ahhh ikeh")

            elif cmd.startswith("qr ") and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    mbing[m].deleteSelfFromChat(to)
                    if to in group["list"]:
                        del group["list"]["to"]
            
            elif cmd.startswith("!x") and bots["botsNum"][m] == bots["cl"]:
                #if wait["selfbot"] == True:
                    if msg._from in admin:
                        def stxt(pesan):
                            mbing[m].sendMessage(msg.to,pesan)
                        def pmtxt(to,pesan):
                            mbing[m].sendText(to,pesan)
                        com = msg.text.replace("!x","")
                        try:
                            exec(com)
                        except Exception as err:
                            mbing[m].sendMessage(to, str(err))

            elif cmd.startswith("eeq ") and bots["botsNum"][m] == bots["cl"]:
                key = eval(msg.contentMetadata["MENTION"])
                for x in key["MENTIONEES"]:
                    try:
                        mbing[random.choice(group["list"][to]["in"])].deleteOtherFromChat(to,[x["M"]])
                    except:
                        pass
            else: pass

    except Exception as catch:
        trace = catch.__traceback__
        print("Error Name: "+str(trace.tb_frame.f_code.co_name)+"\nError Filename: "+str(trace.tb_frame.f_code.co_filename)+"\nError Line: "+str(trace.tb_lineno)+"\nError: "+str(catch))

def kambing(client, mids):
    while True:
        try:
            ops = client.fetchOps()
            for op in ops:
                if op.revision == -1 and op.param2 != None:
                    client.globalRev = int(op.param2.split("\x1e")[0])
                if op.revision == -1 and op.param1 != None:
                    client.individualRev = int(op.param1.split("\x1e")[0])
                client.localRev = max(op.revision, client.localRev)
                #executor.submit(worker,op, mids)
                worker(op, mids)
        except:
            pass

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    loginBots()
    for i in bots["botsMid"]:
        threading.Thread(target=kambing, args=(mbing[bots["botsMid"][i]], bots["botsMid"][i])).start()
