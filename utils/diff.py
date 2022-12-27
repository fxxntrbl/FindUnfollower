def sym_diff(follower: list, following: list) -> list:
    return list(set(follower) ^ set(following))
