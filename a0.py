length = int(input())

print("+", end='')

for i in range(length):
    print("-+")
    print("  "*i, end='')
    print("| |")
    print("  "*i, end='')
    print("+-+", end='')

print()
