def output(input1, input2, input3):
    if input3 == "+":
        return input1 + input2
    elif input3 == "-":
        return input1 - input2
    elif input3 == "*":
        return input1 * input2
    else
        return "Error: bad user"

def main():
    input1 = int(input('Enter your first operand:\n'))
    input2 = int(input('Enter your second operand:\n'))
    input3 = str(input('Enter your desired operator (+, -, or *):\n'))
    print("The result of your calculation is: {}".format(output(input1, input2, input3)))
