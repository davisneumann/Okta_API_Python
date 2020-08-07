import requests, json
from config import token, tenant, headers

first_name = 0
last_name = 0
delete = 0

def main():
    global delete

    login = input("User's login: ")
    content = getUser(login)

    id = content["id"]
    print("User's ID is:\t\t\t\t {:>30}".format(id))

    email = content["profile"]["email"]
    print("User's Email is:\t\t\t {:>30}".format(email))

    fn = content["profile"]["firstName"]
    print("User's firstName value is:\t {0:>30}".format(fn))
    global first_name
    first_name = fn

    ln = content["profile"]["lastName"]
    print("User's lastName value is:\t {:>30}".format(ln))
    global last_name
    last_name = ln

    print("User's status is\t\t\t {:>30}\n".format(content["status"]))

    if content["status"] != "DEPROVISIONED":
        choice = input("Deactivate user and then delete?\n(y/n) ")
        if choice == "y" or choice == "Y":
            delete = 1
            deactivateUser(id)
        else:
            choice = input("Do you want to just deactivate the user?\n(y/n) ")
            if choice == "y" or choice == "Y":
                deactivateUser(id)
            else:
                main()
    else:
        choice = input("User already DEACTIVATED. \nDo you want to DELETE IT?\n(y/n) ")
        if choice == "y" or choice == "Y":
            deleteUser(id)
        elif choice == "n" or choice == "N":
            choice2 = input("What to do, what to do... \nPerhaps you want to REACTIVATE IT?\n(y/n) ")
            if choice2 == "y" or choice2 == "Y":
                reactivateUser(id)
            else:
                main()
        else:
            main()

def getUser(login):
    r = requests.get(f'https://{tenant}.com/api/v1/users?filter=profile.login%20eq%20"{login}"', headers = headers)
    if r.status_code == requests.codes['ok']:
        req = json.loads(r.text)
        try:
            return req[0]
        except IndexError:
            print("Error Occurred! Cannot read / find user. Perhaps this user doesn't exist?")
            main()
    elif r.status_code == 401:
        print("Return error code is 401. Make sure you have a valid API token used in the code.")
        main()
    else:
        print("Unknown Error Occurred! Cannot retrieve user.")
        main()

def deactivateUser(id):
    global delete
    global first_name
    global last_name
    r = requests.post("https://{}.com/api/v1/users/{}/lifecycle/deactivate".format(tenant, id), headers=headers)
    if (r.status_code == requests.codes['ok']):
        print("""Response code is:\t\t\t {0:>30}\n User {2} {1} has just been DEACTIVATED""".format(r.status_code, last_name, first_name))
        if delete == 0:
            main()
        else:
            delete = 0
            deleteUser(id)
    else:
        print("Error occurred. Response code:\n {}".format(r.status_code))
        main()

def deleteUser(id):
    r = requests.delete("https://{}.com/api/v1/users/{}".format(tenant, id), headers=headers)
    if r.status_code == 204:
    #if r.status_code == requests.codes['no_content']:
        print("Response code is:\t\t\t {:>30}\n User has just been DELETED".format(r.status_code))
        main()
    else:
        print("Error occurred. Response code:\n {}".format(r.status_code))
        main()

def reactivateUser(id):
    r = requests.post("https://{}.com/api/v1/users/{}/lifecycle/activate?sendEmail=true".format(tenant,id),headers=headers)
    if r.status_code == requests.codes['ok'] or r.status_code == requests.codes['not_modified']:
        print("Response code is:\t\t\t {:>30}\n User has just been REACTIVATED".format(r.status_code))
        main()
    else:
        print("Error occurred. Response code:\n {}".format(r.status_code))
        main()

main()