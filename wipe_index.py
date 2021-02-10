import os

dir = os.getcwd()+"/index"
for f in os.listdir(dir):
    print("Removing {}".format(f))
    os.remove(os.path.join(dir, f))
    if not os.path.isfile(os.path.join(dir, f)):
        print("successful")
