#!/usr/bin/env python3

import requests

urlroot = "https://passwordstate.blackbaud.com"

key = "fe7263b98c45da372ef9d353b4ac8647"
password = "testpw"
reason = "testing"


def get_password_id(key, list_id, field, value):
    urlpath = "/api/searchpasswords/" + list_id + "?" + field + "=" + value
    header = {'APIKey': key}
    r = requests.get(urlroot + urlpath, headers=header)
    if len(r.json()) > 1:
        raise ValueError("More than 1 item was returned please refine the search or eliminate "
                         "duplicates.")
    elif r.status_code != 200:
        raise ValueError("No results returned please correct your search or check your APIKey.")
    print(r)
    print(r.url)
    print(r.headers)
    print(r.json())
    print(r.json()[0]['PasswordID'])
    return int(r.json()[0]['PasswordID'])


def update_password(key, id, password, reason):
    urlpath = "/api/passwords"
    header = {'APIKey': key, "PasswordID": str(id), "password": password, "reason": reason}
    print(header)
    r = requests.put(urlroot + urlpath, data=header)
    print(r)
    print(r.url)
    print(r.headers)
    print(r.json())

def add_password(key, list_id, title, username, password):
    urlpath = "/api/passwords"
    header = {'APIKey': key, 'PasswordListID': list_id, 'Title': title, 'UserName': username, "password": password}
    print(header)
    r = requests.post(urlroot + urlpath, data=header)
    print(r)
    print(r.url)
    print(r.headers)
    print(r.json())


if __name__ == "__main__":
    pw_id = get_password_id(key, "312", "UserName", "isupdatable")
    update_password(key, pw_id, "BLARG2", "Testing")
    add_password(key, "312", "TestingAdd", "myuser", "testingpwval")