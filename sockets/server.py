import socket
import sqlite3

host = '127.0.0.1'
port = 9000
Max_Connections = 5
usedCities = []

connsql = sqlite3.connect('data.sqlite', check_same_thread=False)
cursor = connsql.cursor()


def TrueCity(city):
    global usedCities
    connsql = sqlite3.connect('data.sqlite', check_same_thread=False)
    cursor = connsql.cursor()
    cursor.execute(f'SELECT city FROM geo WHERE city = "{str(city).capitalize()}" ')
    city1 = cursor.fetchone()
    if city1 is not None:
        if city1[0] not in usedCities:
            if len(usedCities) != 0:
                if str(usedCities[-1][-1].lower()) == "ь" or str(usedCities[-1][-1].lower()) == "ъ" or str(usedCities[-1][-1].lower()) == "ы":

                    if str(usedCities[-1][-2].lower()) == str(city1[0][0].lower()):
                        usedCities.append(city)
                        return city
                    else:
                        print(f"Этот город не начинается с буквы {usedCities[-1][-1].upper()}")
                        return None
                else:

                    if str(usedCities[-1][-1].lower()) == str(city1[0][0].lower()):
                        usedCities.append(city)
                        return city
                    else:
                        print(f"Этот город не начинается с буквы {usedCities[-1][-1].upper()}")
                        return None
            else:
                usedCities.append(city)
                return city
        elif city1[0] in usedCities:
            print("Этот город уже был назван")
            return None

        else:
            print(1)
            return None
    else:
        print("Город введён некорректно. Попробуйте ещё раз:")
        return None


try:
    srv_sock = socket.socket()  # creates a socket
    print("Сокет создан.!")
except Exception as e:
    print("Ошибка создания сокета: ", e)

try:
    srv_sock.bind(("localhost", port))
    print("Сокет подключён по хосту: ", host, " и порту: ", port)
except Exception as e:
    print("ошибка настройки сокета: ", e)
# while True:
srv_sock.listen(Max_Connections)

conn, addr = srv_sock.accept()
print("Успешное соединение : " + str(addr))
while True:
    data = conn.recv(1024).decode()
    print("От клиента: " + str(data))
    usedCities.append(str(data))
    print("Список использованных городов:\n", list(usedCities))
    city = None

    while city is None:
        data = input(' => ')
        city = TrueCity(data)
        if city is not None:
            conn.send(data.encode())
            print("Введённый вами город введён корректно. Ожидайте ответа соперника.")

conn.close()

