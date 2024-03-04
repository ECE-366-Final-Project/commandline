import requests

userID = -1
head = "http://localhost:8080/"

def query(func,payload):
    data = requests.get(head + func, payload)
    return parse(data)

def parse(query_load):
    str_ = query_load.text
    words = str_.split(',')
    return [word.strip(' ') for word in words]

def createAcc():
    username = input("Username: ")
    payload = {"username": username}
    data = query("CreateUser", payload)
    if data[0] in ["400", "500"]:
        print ("ERROR CREATING USER: " + str(data[1:]))
        return
    print("ACCOUNT CREATION SUCCESSFUL")
    return

def logIn():
    username = input("Username: ")
    payload = {"username": username}
    data = query("UserInfo", payload)
    if data[0] in ["400", "500"]:
        print ("ERROR LOGGING IN: " + str(data[1:]))
        return -1
    print("Balance:"+data[2])
    return int(data[1])

def transaction():
    transaction_type = input("Withdraw (w) or Deposit (d): ")
    while(transaction_type not in ['w', 'd']):
        print("INVALID INPUT")
        transaction_type = input("Withdraw (w) or Deposit (d): ")
    amount = input("Amount: ")
    payload = {"userID": userID, "amount":amount}
    if transaction_type == 'd':
        data = query("Deposit", payload)
    elif transaction_type == 'w':
        data = query("Withdraw", payload)
    if data[0] in ["400", "500"]:
        print ("ERROR:" + str(data[1:]))
        return -1
    print("TRANSACTION SUCCESSFUL")
    return

symbols = """1X BAR
2X BAR
3X BAR
SEVEN
BELL
CHERRY
CLOVER
GEM
JACKPOT
LEMON""".split("\n")

def slots():
    bet = input("Bet: ")
    payload = {"userID": userID, "bet":bet}
    data = query("PlaySlots", payload)
    if data[0] in ["400", "500"]:
        print ("ERROR PLAYING SLOTS: " + item+" " for item in data[1:])
        return -1
    data[3] = data[3][:-1]
    while len(data[3]) < 3:
        data[3] = "0"+data[3]
    print(data[3])
    rolls = [symbols[int(i)-1] for i in list(data[3])]
    print("YOU ROLLED:", rolls)
    print("YOUR BET PAID OUT $"+data[1])
    return

while(True):
    print("Options:\n1. Create Account\n2. Log In\n3. Deposit/Withdraw\n4. Play Slots\n5. Quit")
    match(input("Choice: ")):
        case '1':
            createAcc()
        case '2':
            userID = logIn()
        case '3':
            transaction()
        case '4':
            slots()
        case '5':
            break
        case _:
            print("INVALID INPUT")