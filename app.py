import json
import urllib

import requests

options = {
    "userId": "REDECATED",
}  # my id is

config = {
    "followers": {
        "hash": "c76146de99bb02f6415203be841dd25a",
        "path": "edge_followed_by",
    },
    "following": {"hash": "d04b0a864b4b54837c0d870b0e77e076", "path": "edge_follow"},
}

all_users = []


def get_usernames(data):
    user_batch = [element["node"]["username"] for element in data]
    all_users.extend(user_batch)


def make_next_request(next_cursor, list_config):
    params = {
        "id": options["userId"],
        "include_reel": True,
        "fetch_mutual": True,
        "first": 50,
    }
    if next_cursor:
        params["after"] = next_cursor

    query_string = f"https://www.instagram.com/graphql/query/?query_hash={list_config['hash']}&variables={urllib.parse.quote(json.dumps(params))}"

    print(query_string)
    res = requests.get(query_string).json()

    print(res)
    user_data = res["data"]["user"][list_config["path"]]["edges"]
    get_usernames(user_data)

    # print(get_usernames(user_data))

    cursor = ""
    try:
        cursor = res["data"]["user"][list_config["path"]]["page_info"]["end_cursor"]
    except:
        pass

    if cursor:
        make_next_request(cursor, list_config)
    else:
        print("\n".join(all_users))


print("following")
followers = make_next_request("", config["following"])
print("followers")
following = make_next_request("", config["followers"])


# followers = (open("followers.txt", "rt")).read()
# following = (open("following.txt", "rt")).read()

split_f = followers.split("\n")
# split_f.sort()
split_t = following.split("\n")
# split_t.sort()

sym_diff = list(set(split_f) ^ set(split_t))
print(sym_diff)
