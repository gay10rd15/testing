import os
import time

while True:
    print("read, add, remove, make, and delete todo lists")
    time.sleep(1)
    print("press q to quit")
    ui = input()

    if ui == "read":
        fdir = input("Enter the directory of the todo list you want to read: ")
        try:
            with open(fdir, 'r') as f:
                # List comprehension to read, strip, and filter lines
                lines = [line.strip() for line in f if line.strip() and not line.lstrip().startswith('#')]
                for l in lines:
                    print(l)
        except FileNotFoundError:
            print("Could not find file: " + fdir)
        except Exception as e:
            print("An error occurred: " + str(e))
        print()

    elif ui == "add":
        fdir = input("enter the directory of the todo list you want to add to: ")
        try:
            with open(fdir, 'a') as rf:
                item = input("enter the item you want to add: ")
                rf.write(item + "\n")
        except:
            print("could not find file")

    elif ui == "remove":
        fdir = input("enter the directory of the todo list you want to remove from: ")
        try:
            with open(fdir, 'r') as rf:
                items = rf.readlines()
            
            item = input("enter the item you want to remove: ")
            if item + "\n" in items:
                items.remove(item + "\n")
                with open(fdir, 'w') as rf:
                    rf.writelines(items)
            else:
                print("item not found in todo list")
        except:
            print("could not find file")

    elif ui == "make":
        fdir = input("enter the directory of the todo list you want to make: ")
        fdir = fdir + ".txt"
        try:
            rf = open(fdir, 'x')
            rf.close()
        except Exception as e:
            print(e)

    elif ui == "delete":
        fdir = input("enter the directory of the todo list you want to delete: ")
        fdir = fdir + ".txt"
        try:
            os.remove(fdir)
        except:
            print("could not find file")

    elif ui == "q":
        break
    else:
        print("invalid input")
