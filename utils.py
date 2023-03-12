
def is_int(x):
    try:
        int(x)
        return True
    except:
        return False

def is_float(x):
    try:
        float(x)
        return True
    except:
        return False