'''
┏━━━━━━━━━━━━━━━━━
┣[ SDK Squad
┗━━━━━━━━━━━━━━━━━
'''

from linepy import *
from liff.ttypes import LiffChatContext, LiffContext, LiffSquareChatContext, LiffNoneContext, LiffViewRequest
from thrift import transport, protocol, server
from akad.ttypes import *
from akad.ttypes import Message
from akad.ttypes import ContentType as Type
from akad.ttypes import TalkException
from akad.ttypes import IdentityProvider, LoginResultType, LoginRequest, LoginType
from akad.ttypes import ChatRoomAnnouncementContents
from akad.ttypes import Location
from akad.ttypes import ChatRoomAnnouncement
from multiprocessing import Pool, Process
from thrift.Thrift import *
from thrift.unverting import *
from thrift.TMultiplexedProcessor import *
from thrift.TSerialization import *
from thrift.TRecursive import *
from thrift import transport, protocol, server
from thrift.protocol import TCompactProtocol, TMultiplexedProtocol, TProtocol
from thrift.transport import TTransport, TSocket, THttpClient, TZlibTransport
from time import sleep
import pytz, datetime, time, timeit, livejson,asyncio, random, sys, ast, re, os, json, subprocess, threading, string, codecs, requests, ctypes, urllib, traceback, tempfile, platform
from humanfriendly import format_timespan, format_size, format_number, format_length
from datetime import timedelta, date
from datetime import datetime
from threading import Thread, activeCount

#[ SDK Squad _______________________________________________________

_session = requests.session()
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

programStart = time.time()


token = []

apps = {
    "LITE":"ANDROIDLITE\t2.15.0\tAndroid OS\t5.1.1",
    "IOS":"GAK TAU",
    "MAC":"ISI SENDIRI NTOD"
}

admin = ["ue2330fdb6b7db69eb771c3176388d0ff"]
mbing = {}
bots = {
    "cl":0,
    "botsNum":{},
    "botsMid":[],
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
oepoll = {}
blacklist = []
autoPurge = False
loop = asyncio.get_event_loop()

def loginBots():
    for i in range(len(token)):
        tok = token[i]
        app = "DESKTOPMAC"
        if tok.startswith("u"):
            app = "LITE"
        cl = LINE(str(token[i]))
        pf = cl.getProfile()
        mbing[pf.mid] = cl
        bots["botsNum"][pf.mid] = i
        bots["botsMid"].append(pf.mid)
        bots["teams"][pf.mid] = []
        oepoll[pf.mid] = OEPoll(cl)
        cekGroup(cl, pf.mid)
        #checkContact(cl, admin)
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
        client.kickoutFromGroup(to, [j])

def goQR(client, to, act):
    try:
        G = client.getGroup(to)
        G.preventedJoinByTicket = act
        client.updateGroup(G)
    except:
        pass

def goKick(to, enemy):
    if len(group["list"][to]["in"]) > 0:
        try:
            mbing[random.choice(group["list"][to]["in"])].kickoutFromGroup(to, [enemy])
        except:
            pass

def goCancel(to, enemy):
    if len(enemy) > 34:
        x = (len(enemy)//33)
        if len(group["list"][to]["in"]) > 0:
            for i in range(x):
                try:
                    mbing[random.choice(group["list"][to]["in"])].cancelGroupInvitation(to, [enemy[i*33:i*33+33]])
                except:
                    pass
    else:
        if len(group["list"][to]["in"]) > 0:
            try:
                mbing[random.choice(group["list"][to]["in"])].cancelGroupInvitation(to, [enemy])
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
            client.acceptGroupInvitation(to)
            apdetGroup(to, myself, "in")
            if autoPurge == True:
                purge(client, to)

def peroCancel(to, enemy, victim, myself):
    if victim == myself and enemy not in group["sdk"]:
        if len(group["list"][to]["in"]) > 0:
            bots["cl"] = bots["botsNum"][random.choice(group["list"][to]["in"])]
        goKick(to, enemy)
        if len(group["list"][to]["out"]) > 0:
            mbing[random.choice(group["list"][to]["in"])].inviteIntoGroup(to, group["list"][to]["out"])
        belekin(enemy)
    else:
        if to in group["invite"] or victim in bots["sdk"]:
            if enemy not in bots["sdk"]:
                goKick(to, enemy)
                if victim in bots["botsMid"] and len(group["list"][to]["in"]) > 0 and len(group["list"][to]["out"]) > 0:
                    mbing[random.choice(group["list"][to]["in"])].inviteIntoGroup(to, group["list"][to]["out"])
                belekin(enemy)

def peroKick(to, enemy, victim, myself, num):
    if victim == myself and enemy not in bots["sdk"]:
        apdetGroup(to, myself, "out")
        if num == bots["cl"] and len(group["list"][to]["in"]) > 0:
            bots["cl"] = bots["botsNum"][random.choice(group["list"][to]["in"])]
        goKick(to, enemy)
        if len(group["list"][to]["out"]) > 0 and len(group["list"][to]["in"]) > 0:
            mbing[random.choice(group["list"][to]["in"])].inviteIntoGroup(to, group["list"][to]["out"])
        belekin(enemy)
    else:
        if to in group["kick"] or victim in bots["sdk"]:
            if enemy not in bots["sdk"]:
                if victim not in bots["botsMid"] and len(group["list"][to]["in"]) > 0:
                    goKick(to, enemy)
                    mbing[random.choice(group["list"][to]["in"])].inviteIntoGroup(to, [victim])
                    belekin(enemy)

def peroJoin(to, enemy):
    if to in group["join"] or enemy in blacklist:
        if len(group["list"][to]["in"]) > 0:
            goQR(mbing[random.choice(group["list"][to]["in"])], to, True)
            goKick(to, enemy)
            belekin(enemy)

def cekGroup(client, myself):
    x = client.getGroupIdsJoined()
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

def restartProgram():
    print('\n》》》》PROGRAM RESTARTED《《《《\n')
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)

def runtime(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weeks, days = divmod(days,7)
    months, weeks = divmod(weeks,4)
    text = ""
    if months != 0: text += "%02d Months" % (months)
    if weeks != 0: text += " %02d Weeks" % (weeks)
    if days != 0: text += " %02d Days" % (days)
    if hours !=  0: text +=  " %02d Hours" % (hours)
    if mins != 0: text += " %02d Minutes" % (mins)
    if secs != 0: text += " %02d Seconds" % (secs)
    if text[0] == " ":
        text = text[1:]
    return text

#[ SDK Squad _______________________________________________________

def logError(client, text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Jakarta")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("logError.txt","a") as error:
        error.write("\n[ {} ] {}".format(str(time), text))

#[ SDK Squad _______________________________________________________

def sendMention(client, to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@Mbing"
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)

#[ SDK Squad _______________________________________________________

def sendTemplate(client, group, data):
    xyz = LiffChatContext(group)
    xyzz = LiffContext(chat=xyz)
    view = LiffViewRequest('1602687308-GXq4Vvk9', xyzz)
    token1 = client.liff.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))

def sendTemplate(client, to, data):
    xyz = LiffChatContext(to)
    xyzz = LiffContext(chat=xyz)
    view = LiffViewRequest('1602687308-GXq4Vvk9', xyzz)
    token = client.liff.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))

def mbingFlex(client, to, data):
    data={"type":"flex","altText":"KAMBING SQUAD","contents":data}
    sendTemplate(client, to, data)

def mbingSticker(client, to, url):
    data={
        "type": "template",
        "altText": "Mbing SDK mengirim sticker",
        "baseSize": {
            "height": 1040,
            "width": 1040
        },
        "template": {
            "type": "image_carousel",
            "columns": [{
                "imageUrl": url,
                "action": {
                    "type": "uri",
                    "uri": "https://vx6-ct.com",
                    "area": {
                        "x": 520,
                        "y": 0,
                        "width": 520,
                        "height": 1040
                    }
                }
            }]
        }
    }
    sendTemplate(client, to, data)

def allowLiff(client):
    url = 'https://access.line.me/dialog/api/permissions'
    data = {
        'on': [
            'P',
            'CM'
        ],
        'off': []
    }
    headers = {
        'X-Line-Access': client.authToken,
        'X-Line-Application': client.server.APP_NAME,
        'X-Line-ChannelId': '1602687308',
        'Content-Type': 'application/json'
    }
    requests.post(url, json=data, headers=headers)

def sendFooter(client, receiver, text):
    label = settings["label"]
    icon = settings["iconUrl"]
    link = settings["linkUrl"]
    data = {
        "type": "text",
        "text": text,
        "sentBy": {
            "label": "{}".format(label),
            "iconUrl": "{}".format(icon),
            "linkUrl": "{}".format(link)
        }
    }
    sendTemplate(client, receiver, data)

def randomSticker(client, to, packageId):
    r = requests.get("https://vx6-ct.com/bot/sticker.php?id=" + packageId).json()
    x = [x["id"] for x in r]
    x.remove(packageId)
    if type(to) is list:
        for i in to:
            client.sendSticker(i, packageId, random.choice(x))
    else:
        client.sendSticker(to, packageId, random.choice(x))

def getMessageId(client, to, messageId):
    try:
        res = [x for x in client.getRecentMessagesV2(to, 999) if x.id == messageId]
    except Exception as asu:
        res = asu
    return res

#[ SDK Squad _______________________________________________________

async def kambing(op, m):
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
                    ass = mbing[m].sendMessage(to,'BACOD')
                    #print(ass)

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
                        mbing[m].kickoutFromGroup(to,[m])
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
                        mbing[m].inviteIntoGroup(to, bots["teams"][m])
                        mbing[m].sendMessage(to, "Ahhh ikeh")

            elif cmd == "allin" and bots["botsNum"][m] == bots["cl"]:
                if sender in admin:
                    if len(bots["botsMid"]) > 0:
                        x = []
                        for i in bots["botsMid"]:
                            if m != i:
                                x.append(i)
                        mbing[m].inviteIntoGroup(to, i)
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
                        mbing[random.choice(group["list"][to]["in"])].kickoutFromGroup(to,[x["M"]])
                    except:
                        pass
            else: pass
        else: pass
    except Exception as error:
        logError(mbing[m], error)
        traceback.print_tb(error.__traceback__)

#[ SDK Squad _______________________________________________________

def run(mids):
    while True:
        try:
            ops = oepoll[mids].singleTrace(count=50)
            if ops != None:
                for op in ops:
                    loop.run_until_complete(kambing(op, mids))
                    oepoll[mids].setRevision(op.revision)
        except Exception as error:
            logError(mbing[mids].error)

#[ SDK Squad _______________________________________________________

if __name__ == '__main__':
    loginBots()
    for i in bots["botsMid"]:
        run(i)
        threading.Thread(target=loop.run_until_complete(kambing(op, i))).start()
