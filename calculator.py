import re
import sys
import csv


file_path = "calc_memory.csv"

def main():
    loop_calculator()


def loop_calculator():

    while True:
        i = input("Enter a expression or give a command (HELP for options): ").strip()

        if(check_commands(i)):
            continue

        try:
            num1, operation, num2 = try_get_values(i)
            calculate_operation(num1, operation, num2)
        except TypeError:
            pass

        #if(try_get_values(i) != None):
        #    num1, operation, num2 = try_get_values(i)
        #    calculate_operation(num1, operation, num2)
        #else:
        #    continue


def try_get_values(i):
    values = re.search(r"^(\d+(?:\.\d*)?)(?: )?([+\-*/])(?: )?(\d+(?:\.\d*)?)$", i)
                         #(1stNum)(optionalSpace)(operation)(optionalSpace)(2ndNum)

    if(values): #If values not empty, and its matchs are the right syntax
        #print(values.groups()) #Debug
        return (values.group(1)), values.group(2), values.group(3)
    elif not(values):
        print("Error, invalid prompt! Try again")
        return None


def calculate_operation(n1, o, n2):
    if(n1.__contains__(".") or n2.__contains__(".")):
        number1 = float(n1)
        number2 = float(n2)
    else:
        number1 = int(n1)
        number2 = int(n2)

    if(o =="+"):
        result = number1 + number2
    elif(o =="-"):
        result = number1 - number2
    elif(o =="*"):
        result = number1 * number2
    elif(o =="/"):
        try:
            result = number1 / number2
        except ZeroDivisionError:
            result = 0

    print(f"Your operation was: {number1} {o} {number2}")
    print("Your answer is:", result, "\n")

    save_calculation(number1, o, number2, result)


def save_calculation(n1, op, n2, result):
    data = {"number1":n1, "operation":op, "number2":n2, "result":result}

    if(file_exists_check()):
        mode = 'a'
    else:
        mode = 'w'

    file_w = open(file_path, "a", newline='')
    f_names = ["number1", "operation", "number2", "result"]
    writer = csv.DictWriter(file_w, fieldnames=f_names)

    if(mode == "w"):
        writer.writeheader()

    #Check how many lines there are already:
    line_amount = 0
    file_r = open(file_path, "r", newline='')
    reader = csv.DictReader(file_r)
    for _ in reader:
        line_amount+=1

    if(line_amount-1 < 10):
        writer.writerow(data)

    file_r.close()
    file_w.close()


def file_exists_check():
    try:        
        f = open(file_path, "r")
        f.close()
        #print("Exists!")
        return True
    
    except FileNotFoundError:
        #print("Doesnt exist!")
        return False


def check_commands(input):
    match(input):
        case "OFF" | "off":
            sys.exit("...Turning off...")
            return True
        case "MEMORY" | "memory":
            print("...Checking Memory...")
            load_calculations()
            return True
        case "CLEAR" | "clear":
            print("...Clearing Memory...")
            clear_calculations()
            return True
        case "HELP" | "help":
            print("\n   Following Commands:")
            print("1. OFF = Turns off calculator")
            print("2. MEMORY = Outputs all saved expressions")
            print("3. CLEAR = Delete all saved expressions\n")
            return True
        case _:
            return False
        

def load_calculations():
    if(file_exists_check()):
        f = open(file_path,"r")
        reader = csv.DictReader(f)

        for row in reader:
            num1 = row['number1']
            num2 = row['number2']
            op = row['operation']
            result = row['result']

            if(result.__contains__(".")):
                result = float(result)
                result = round(result, 2)

            print(f"{num1} {op} {num2} = {result}")
        f.close()
    else:
        print("No memory detected")


def clear_calculations():
    if(file_exists_check()):#Reset file
        file = open(file_path, "w", newline='')
        f_names = ["number1", "operation", "number2", "result"]
        writer = csv.DictWriter(file, fieldnames=f_names)
        writer.writeheader()
    


if(__name__=="__main__"):
    main()
