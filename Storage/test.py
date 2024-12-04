from pathlib import Path

if __name__ == "__main__":
    p = Path("C:\\Users\\Christopher Cyr\\Documents\\School\\First Year\\Winter\\ICS 32\\a4")
    p = p.joinpath("ISO 3166-1.txt")
    f = p.open("r")
    contents = f.readlines()
    f.close()
    f = p.open("w")
    count = 0
    for line in contents:
        if len(line) == 3:
            f.write(line)
        else:
            new_line = line.split(' ')
            for i in new_line:
                if len(i) == 3:
                    f.write(i)
    f.close()