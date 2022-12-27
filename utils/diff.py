followers = (open("followers.txt", "rt")).read()
following = (open("following.txt", "rt")).read()

split_f = followers.split("\n")
# split_f.sort()
split_t = following.split("\n")
# split_t.sort()

sym_diff = list(set(split_f) ^ set(split_t))
print(sym_diff)
