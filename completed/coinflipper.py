import random, time as T, argparse

parser = argparse.ArgumentParser()
parser.add_argument("times", help="the number of times you want to flip a coin")
args = parser.parse_args()
num = 0; cf = []

if args.times:
    try:
        int(args.times)
    except:
        print("you must enter a number")
    ui = args.times
else:
    while True:
        ui = input("enter the number of times you want to flip a coin:\n>")
        try:
            int(ui)
            break
        except ValueError:
            print("you must enter a number")
while int(num) < int(ui):
    fr = random.randint(1,2)
    cf.append(fr)
    num += 1
c = cf.count(1)
int(c)
if c > int(ui) / 2:
    print("heads was flipped more")
elif c < int(ui) / 2:
    print("tails was flipped more")
else:
    print("its a tie")
#print(cf) # print all the numbers generated
