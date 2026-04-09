print("[LOADING]: CLI module...", end="")

def __init__(string):
    system(string)

def out(string):
    print("  ", string, flush=True)

def system(string):
    print("[SYSTEM]:", string, flush=True)

def cache(string):
    print("[CACHE]:", string, flush=True)

def test(string):
    print("[TEST]:", string, flush=True)

def error(string):
    print("[ERROR]:", string, flush=True)

print('good')