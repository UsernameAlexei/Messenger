#Загружаем библиотеку фласк
#Берем простой пример с сайта
import time

from flask import Flask, request, abort
import datetime

app=Flask(__name__)

#создаем массивчик в который будем складывать сообщения
#здесь будут храниться сообщения
#словарик в котором храняться словарики
messages=[
    {'username':'Nick', 'text':'Hello', 'time': 0.0}
]

#сделаем авторизацию для сайта
#словарик с паролями
users={
    'Nick':'12345'
}

#@app декоратор
#по адресу / создалась страничка с надписью hello, world!
@app.route("/")
def hello():
    return"Hello,World!"

#создаем страничку с адресом /status
@app.route("/status")
def status():
    return {
        'status':True,
        'name':'Skillbox messenger', #имя нашего сервера
        'time': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), #добавляем время и форматирование времен
        'messages_count':len(messages),
        'users_count': len(users)
    }

#пишем метод для отправки сообщений
@app.route('/send', methods=['POST'])
def send():
    username=request.json['username']
    password = request.json['password']

#проверяем никнейм
    if username in users: #если зарегистрированный проводим авторизацию
        if password != users[username]:
            return abort(401)
        else: #новый пользователь, регистрируем
            users[username] = password


    text=request.json['text']
    current_time= time.time()#пишет количество секунд которых прошло, с момента начала unix эпохи 1янв 1970 года
    message={'username':username, 'text':text, 'time':current_time}#из объектов собираем сообщение,которое состоит из ключей
    messages.append(message)#добавляет сообщения в переменную
    print(messages)#для теста, будет печатать все сообщения которые есть  на сервере
    return {'ok':True}
# так мы сформирвали сообщение

#вывод наших сообщений и сообщений других участников
@app.route('/messages') #метод GET т.к мы не отправляем, а только запрашиваем данные
def messages_view():
    after=float(request.args.get('after'))#достаем параметры из запроса
    #т.к параметр строка, нужно перевести к float

   # filtered_messages=[]
    #пробежимся по всем сообщениям
   # for message in messages:
   #     if message['time'] >after: #если у сообщения есть параметр тайм
   #         filtered_messages.append(message) #добавим сообщение

    #list comprehension - объявление списка
    filtered_messages = [message for message in messages if message['time'] >after ]

    #возвращаем список всех сообщений которые есть у нас на сервере
    return {
        'messages':filtered_messages
    }

#ввод параметра с указанием сообщений которые мы хотим получать

app.run()                    