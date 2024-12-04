# Chris Cyr
# cyrc@uci.edu
# 12436037

from pathlib import Path

if __name__ == "__main__":
    cap = 10**9
    print("Generating primes")
    primes = []
    for possiblePrime in range(2, cap + 1):
        isPrime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                isPrime = False
                break
        if isPrime:
            primes.append(possiblePrime)
    print("Primes generated")
    p = Path()
    p = p.joinpath("collatz.txt")

    with p.open("a") as f:
        for init in primes:
            current = init
            topvalue = init
            steps = 0
            topstep = 0
            while current != 1:
                if current % 2 == 1:
                    current *= 3
                    current += 1
                else:
                    current /= 2
                
                if current >= topvalue:
                    topvalue = current
                    topstep = steps
                
                steps += 1

                if steps == 10**6:
                    print("Stopping after 1 million steps.")
                    print(f"Collatz conjecture not clear for {init}")
                        
            if current == 1:
                f.write(f"Start: {init}, Steps: {steps}, Max: {topvalue} at {topstep}\n")
    print("All done")



"""
def create_file(location: Path, options: dict):
    if "-n" in options.keys():
        p = location.joinpath(f"{options['-n']}.dsu")
        if p.exists():
            print("ERROR: File already exists, opening")
            open_file(p)
            return
        else:
            p.touch()
        print(p, "successfully created")

        """