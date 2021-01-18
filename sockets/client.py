import socket
import sqlite3

host = '10.5.1.84'
port = 9000
usedCities = []

cli_sock = socket.socket()
cli_sock.connect(("localhost", port))

connsql = sqlite3.connect('data.sqlite', check_same_thread=False)
cursor = connsql.cursor()

def TrueCity(city):
    connsql = sqlite3.connect('data.sqlite', check_same_thread=False)
    cursor = connsql.cursor()
    global usedCities
    cursor.execute(f'SELECT city FROM geo WHERE city = "{str(city).capitalize()}" ')
    city1 = cursor.fetchone()
    if city1 is not None:
        if city1[0] not in usedCities:
            if len(usedCities) != 0:
                if str(usedCities[-1][-1].lower()) == "ь" or str(usedCities[-1][-1].lower()) == "ъ" or str(
                        usedCities[-1][-1].lower()) == "ы":

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

city = None

while city is None:
    data = input(' => ')
    city = TrueCity(data)
    if city is not None:
        cli_sock.send(data.encode())
        print("Введённый вами город введён корректно. Ожидайте ответа соперника.")


while str(data) != "bye":
    data = cli_sock.recv(1024).decode()
    print("От сервера: " + str(data))
    usedCities.append(str(data))
    print("Список использованных городов:\n", list(usedCities))

    city = None

    while city is None:
        data = input(' => ')
        print(str(data))
        city = TrueCity(data)
        if city is not None:
            cli_sock.send(data.encode())
            print("Введённый вами город введён корректно. Ожидайте ответа соперника.")

cli_sock.close()