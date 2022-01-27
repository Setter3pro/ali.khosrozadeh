import json
import requests
import os
from flask import Flask
from flask import request
from flask import Response
from bs4 import BeautifulSoup

url = "https://api.telegram.org/bot5126622867:AAFPuEpez60x7-pCy6cZRbRY2BH-eMheblU/"
api = ""

app = Flask(__name__)

def get_all_updates():
    response = requests.get(url + 'getUpdates')
    return response.json()

def get_last_update(allUpdates):
    return allUpdates['result'][-1]

def get_chat_id(update):
    return update['message']['chat']['id']

def sendMessage(chat_id, text):
    sendData = {
        'chat_id' : chat_id,
        'text' : text,
    }
    response = requests.post(url + 'sendMessage', sendData)
    return response


def send_photo(chat_id, file_opened):
    method = "sendPhoto"
    params = {'chat_id': chat_id}
    files = {'photo': file_opened}
    resp = requests.post(url + method, params, files=files)
    return resp

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text', '')
        if text == '/start':
            sendMessage(chat_id, f'Welcome to iust_filmyab_10.a.abot!\nhere you can do multiple things:\n\n1_ search movies by command below:(ensure that you enter the name correctly:) )\n\n/search "name of the movie, series, TV shows and..."\n\n\n\n2_ choose genres and see a list of the best products in those genres! command as shown below:\n\n /genre "genres you like with a space between them"\nvalid genre inputs are shown below:\n\n| action | adventure | animation |\n| biography | comedy | crime |\n| documentary | drama | family |\n| fantasy | film_noir |game_show |\n| history | horror | music | musical |\n| mystery | news | reality_tv | romance |\n| sci_fi | sport | talk_show | thriller | war |\n | western |\n*movies that are shown are the most papular ones in top 250 IMDB!\n\n\n\n3_ You can make a list of your favorit movies! you can do it with the commands below:\n\n/add "favorit movie"\n/delete "movie which exists in your list"\n/list --> you can see your current list with this command!')
        elif '/genre' in text:
            a = text.split()
            a.pop(0)

            def moratab(a):
                p = []
                count = 0
                for m in range(25):
                    p.append(str(count))
                    count += 1
                for i in a:
                    i = i.lower()
                    if i == 'action':
                        p[0] = i
                    elif i == 'adventure':
                        p[1] = i
                    elif i == 'animation':
                        p[2] = i
                    elif i == 'biography':
                        p[3] = i
                    elif i == 'comedy':
                        p[4] = i
                    elif i == 'crime':
                        p[5] = i
                    elif i == 'documentary':
                        p[6] = i
                    elif i == 'drama':
                        p[7] = i
                    elif i == 'family':
                        p[8] = i
                    elif i == 'fantasy':
                        p[9] = i
                    elif i == 'film_noir':
                        p[10] = i
                    elif i == 'game_show':
                        p[11] = i
                    elif i == 'history':
                        p[12] = i
                    elif i == 'horror':
                        p[13] = i
                    elif i == 'music':
                        p[14] = i
                    elif i == 'musical':
                        p[15] = i
                    elif i == 'mystery':
                        p[16] = i
                    elif i == 'news':
                        p[17] = i
                    elif i == 'reality_TV':
                        p[18] = i
                    elif i == 'romance':
                        p[19] = i
                    elif i == 'sci_fi':
                        p[20] = i
                    elif i == 'sport':
                        p[21] = i
                    elif i == 'talk_show':
                        p[22] = i
                    elif i == 'thriller':
                        p[23] = i
                    elif i == 'war':
                        p[24] = i
                    elif i == 'western':
                        p[25] = i
                pp = []
                for i in p:
                    if i.isnumeric() is False:
                        pp.append(i)
                return (pp)

            moratab(a)
            x = ''
            z = ''
            for i in moratab(a):
                x = x + ',' + i.lower()
            x = x.lstrip(',')
            page = requests.get(
                f'https://www.imdb.com/search/title/?genres={x}&groups=top_250&sort=moviemeter,desc&count=250')
            soup = BeautifulSoup(page.text, 'html.parser')
            q = soup.find_all(class_="lister-item-header")
            h = soup.find_all(class_="inline-block ratings-imdb-rating")
            count1 = 0
            for i in q:
                i = list(i)
                i[3] = str(i[3])
                count = 0
                x = 0
                while x != '>':
                    x = i[3][count]
                    count += 1
                u = i[3][count:len(i[3])]
                u = u.rstrip('</a>')
                h[count1] = list(h[count1])
                h[count1][3] = str(h[count1][3])
                count = 0
                x = 0
                while x != '>':
                    x = h[count1][3][count]
                    count += 1
                v = h[count1][3][count:len(i[3])]
                v = v.rstrip('</strong>')
                z = z + '\n' + '\n' + u + '\n' + 'IMDB: ' + v
                count1 += 1
            sendMessage(chat_id, z)

        elif '/search' in text:
            b = text.split()
            b.pop(0)
            x = ''
            for i in b:
                x = x + '+' + i.lower()
            x = x.lstrip('+')
            page = requests.get(f'https://www.imdb.com/find?q={x}&ref_=nv_sr_sm')
            soup = BeautifulSoup(page.text, 'html.parser')
            q = soup.find_all(class_="result_text")
            h = soup.find_all(class_="inline-block ratings-imdb-rating")
            q = list(q)
            q[0] = str(q[0])
            q[0] = q[0][34:len(q[0])]
            count = 0
            while True:
                if q[0][count] == '"':
                    q[0] = q[0][:count]
                    break
                count += 1
            q[0] = 'http://imdb.com' + q[0] + '?ref_=fn_al_tt_1'
            w = q[0]
            ##
            page = requests.get(w)
            soup = BeautifulSoup(page.text, 'html.parser')
            q = soup.find_all(class_="GenresAndPlot__TextContainerBreakpointXS_TO_M-sc-cum89p-0 kHlJyu")
            q = str(q)
            x = 0
            count = 0
            while x != '>':
                x = q[count]
                count += 1
            u = q[count:len(q)]
            u = u.rstrip('</span>]')
            if u[len(u) - 7: -1] == 'ead al':
                u = u.rstrip(
                    '...<!-- --> <a class="ipc-link ipc-link--baseAlt" data-testid="plot-read-all-link" href="plotsummary?ref_=tt_ov_pl">Read all')

            page = requests.get(w)
            soup = BeautifulSoup(page.text, 'html.parser')
            q = soup.find_all(class_="ipc-lockup-overlay ipc-focusable")
            count = 0
            x = 0
            q[0] = str(q[0])
            while x != 'ref="':
                x = q[0][count] + q[0][count + 1] + q[0][count + 2] + q[0][count + 3] + q[0][count + 4]
                count += 1
            s = q[0][count + 4:len(q[0])]
            s = s.rstrip('?ref_=tt_ov_i"><div class="ipc-lockup-overlay__screen"></div></a>') + '/'
            pic_link = f'http://imdb.com{s}'
            page_pic = requests.get(pic_link)
            soup = BeautifulSoup(page.text, 'html.parser')
            p = soup.find_all(class_="Media__PosterContainer-sc-1x98dcb-1 dGdktI")
            count = 0
            x = 0
            p = str(p)
            if p == '[]':
                sendMessage(chat_id, 'Unfortunately could not download the poster:(')
                sendMessage(chat_id, u + ' ...')
            else:
                while x != '285w,':
                    x = p[count] + p[count + 1] + p[count + 2] + p[count + 3] + p[count + 4]
                    count += 1
                s = p[count + 4:len(p)]
                count = 0
                x = 0
                while x != '380w':
                    x = s[count] + s[count + 1] + s[count + 2] + s[count + 3]
                    count += 1
                s = s[:count - 1]
                pic = requests.get(s)
                pic = pic.content
                send_photo(chat_id, pic)
                sendMessage(chat_id, u + ' ...')

        elif '/add' in text:
            a = text[5:]
            username = msg['message']['from']['username']
            favorit = read_json()
            if username not in favorit.keys():
                favorit[username] = []
            favorit[username].append(a)
            write_json(favorit)
            sendMessage(chat_id, 'Added to favorits list!')
        elif text == '/list':
            favorit = read_json()
            username = msg['message']['from']['username']
            if username not in favorit.keys():
                sendMessage(chat_id, 'Favorits list is empty!')
            elif favorit[username] == []:
                sendMessage(chat_id, 'Favorits list is empty!')
            else:
                z = ''
                for i in favorit[username]:
                    z = z + '\n' + i
                sendMessage(chat_id, z)

        elif '/delete' in text:
            a = text[8:]
            favorit = read_json()
            username = msg['message']['from']['username']
            if a not in favorit[username]:
                sendMessage(chat_id, 'this movie is not in your list!')
                pass
            else:
                favorit[username].remove(a)
                sendMessage(chat_id, 'deleted')
                write_json(favorit)

        return Response('ok', status = 200)
    else:
        return "<h1>Hi! Im a Bot</h1>"


def write_json(data, filename='fav.json'):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)


def read_json(filename='fav.json'):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data


write_json({})
app.run(host = "0.0.0.0", port = int(os.environ('PORT',5000)))








