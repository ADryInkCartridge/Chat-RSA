from random import randrange

def read_primes(filename = "primes.txt"):
    with open(filename, "r") as file:
      line = file.read()
      primes = line.split(",")
      primes = [int(prime) for prime in primes]
    return primes


def gcd(a, b):
  # GCD(a, b) = GCD(b, a mod b)
  while b != 0:
    a, b = b, a % b
  return a

def coprime(a, b):
  return gcd(a, b) == 1

def modinv(a, m):
  # Compute the modular multiplicative inverse of a modulo m
  # using the extended Euclidean algorithm
  if coprime(a, m):
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    # mathemagics
    # print("u1: " + str(u1) + " u2: " + str(u2) + " u3: " + str(u3) + " v1: " + str(v1) + " v2: " + str(v2) + " v3: " + str(v3))
    while v3 != 0:
      q = u3 // v3
      v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
      # print("u1: " + str(u1) + " u2: " + str(u2) + " u3: " + str(u3) + " v1: " + str(v1) + " v2: " + str(v2) + " v3: " + str(v3))
    return u1 % m
  else:
    return None

# for dummies  
def simple_modinv(a,m):
  for i in range(1,m):
    if (a*i)%m == 1:
      return i
  return None

def generate_keys():
  # Generate the public and private keys for the RSA algorithm
  primes = read_primes()
  p = randrange(0, 30)
  q = randrange(p, 50)

  p = primes[p]
  q = primes[q]

  n = p * q
  phi_n = (p - 1) * (q - 1)
  e = randrange(1, phi_n)
  while not coprime(e, phi_n):
    e = randrange(1, phi_n)
    
  d = modinv(e, phi_n)
  public_key = (n, e)
  private_key = (n, d)
  return (public_key, private_key)


# print(generate_keys())