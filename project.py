import os
import socket
import subprocess
import datetime
import json


def currentTime():
    timenow = datetime.datetime.now()
    return [timenow.strftime("%m-%d-%y-"),
            timenow.strftime("%x %I:%M:%S %p"),
            timenow.strftime("%I:%M:%S%p")]


def createLog():
    log_file = os.path.expanduser(r"~\Documents\{}log.txt".format(currentTime()[0]))
    if os.path.exists(log_file) is False:
        with open(log_file, "w") as log:
            log.close()
    else:
        pass
        # print("file exist")


def checkip():
    log_file = os.path.expanduser(r"~\Documents\{}log.txt".format(currentTime()[0]))
    with open(log_file, "r") as read_log:
        print(read_log.read())


def isvalid(ip):
    try:
        socket.inet_aton(str(ip))
        return True
    except socket.error:
        return False


def ping(ip):
    a = subprocess.Popen("ping -w 1 {}".format(ip), shell=True, stdout=subprocess.PIPE)
    x = a.communicate()[0].decode()
    try:
        loss = x.split()[x.split().index("loss),") - 1].strip('(').strip('%')
        loss = int(loss)
        if loss == 100:
            return "100% Reply"
        elif loss == 75:
            return "75% Reply"
        elif loss <= 50:
            return "{}% Reply |Needs Attention|".format(loss)
        else:
            return "Contact Administration."
    except Exception:
        return "Could not find host"


def network():  # uses arp -a to display the network, it's then parsed and placed in a list
    global IPs
    IPs = []
    a = subprocess.Popen("arp -a", shell=True, stdout=subprocess.PIPE)
    x = a.communicate()[0].decode()
    for i in x.split():
        if isvalid(i) is True:
            IPs.append(i)
        else:
            pass


def showPings():
    try:
        for i in IPs:
            print("{} {}".format(i, ping(i)))
    except NameError:
        network()
        for i in IPs:
            try:
                print("{} {}".format(i, ping(i)))
            except KeyboardInterrupt:
                break


def showNetwork():
    try:
        for i in IPs:
            print("{}".format(i))
    except NameError:
        network()
        for i in IPs:
            print("{}".format(i))


def logIP():
    log_file = os.path.expanduser(r"~\Documents\{}log.txt".format(currentTime()[0]))
    network()
    with open(log_file, "w") as log:
        for i in IPs:
            print("{} {}\n".format(i, ping(i)))
            log.write("{} {}\n".format(i, ping(i)))

    print("IPs status log was created!")


def menu():
    adminCred = os.path.expanduser(r"~\Documents\admincred.json")
    if os.path.exists(adminCred) is False:
        open(adminCred, "w")
        with open(adminCred) as r:
            try:
                data = json.load(r)
            except Exception:
                print("No available username and password, setting default to User1 and User1pass.\n")
        with open(adminCred, "w") as w:
            up = {"User1": "User1pass"}
            json.dump(up, w)
        with open(adminCred) as r:
            data = json.load(r)
    else:
        with open(adminCred) as r:
            data = json.load(r)


    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()
    if username in data and password == data.get(username):
        login = True
        while login is True:
            try:
                options = int(input(
                            "\n1 - Show Current Network\n"
                            "2 - Ping A Single IP Address\n"
                            "3 - Show Network Status\n"
                            "4 - Rescan Network\n"
                            "5 - Create Log\n"
                            "6 - Add User\n"
                            "7 - Delete User\n"
                            "0 - Quit\n"
                            "What would you like to do: "))
            except ValueError:
                continue
            if options == 1:
                showNetwork()

            elif options == 2:
                target = input("What IP Address would you like to ping: ")
                print(target, ping(target))

            elif options == 3:
                showPings()

            elif options == 4:
                network()
                print("Rescan Complete...")

            elif options == 5:
                createLog()  # creates file
                logIP()  # writes in file

            elif options == 6:
                print("Please reenter admin credentials.")
                username = input("Enter Username: ").strip()
                password = input("Enter Password: ").strip()
                if username in data and password == data.get(username):
                    nUser = input("\nEnter New Username: ").strip()
                    nPass = input("Enter New Password: ").strip()
                    joint = {nUser: nPass}
                    data.update(joint)
                    print("User {} was added".format(nUser))
                else:
                    print("Unnable to process this request")

            elif options == 7:
                print("Please reenter admin credentials.")
                username = input("Enter Username: ").strip()
                password = input("Enter Password: ").strip()
                if username in data and password == data.get(username):
                    targetUser = input("Enter the username of the account to be deleted: ").strip()
                    targetPass = input("Enter the password of the account to be deleted: ").strip()
                    if len(data) > 1:
                        if targetUser in data and targetPass == data.get(targetUser):
                            del data[targetUser]
                            print("The user |{}| has been deleted.".format(targetUser))
                        else:
                            print("The username {} does not exist.".format(targetUser))
                    else:
                        print("Can't Remove this log in.")
                else:
                    print("Incorrect Admin credentials.")
            elif options == 0:
                print("Quiting...")
                login = False
    else:
        print("Incorrect Username or Password")

    with open(adminCred, "w") as w:
        json.dump(data, w)


menu()

