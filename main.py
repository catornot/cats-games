import time
import importlib
import sys

with open("test.py","r") as code:
    content = code.read()

with open("test.py","w") as code:
    code.write("")

try:
    import test
except:
    print("Import error")
    sys.exit()

with open("test.py","w") as code:
    code.write(content)



start = time.time()
error = False

while time.time() < start + 30:

    try:
        importlib.reload(test)
    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)

    try:
        import test
        test.Test(test = "huh")


    except Exception as e:
        if hasattr(e, 'message'):
            print(e.message)
        else:
            print(e)