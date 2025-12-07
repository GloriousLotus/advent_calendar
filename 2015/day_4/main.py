from hashlib import md5

#input
secret_key = "ckczppom"

#helper
enc = lambda n:md5((secret_key+str(n)).encode()).hexdigest()

#part 1
n=0
h = enc("")

while h[:5] != "00000":
    n = n+1
    h = enc(n)

print(f"Solution part one:{n}")

#part 2
n=0
h = enc("")

while h[:6] != "000000":
    n = n+1
    h = enc(n)

print(f"Solution part two:{n}")
