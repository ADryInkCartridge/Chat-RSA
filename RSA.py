def RSA_Encrypt(data):
    public_keys, message = data
    print(public_keys, message, "IN RSA")
    n, e = public_keys
    encrypted = []
    for char in message:
        encrypted.append((ord(char) ** e) % n)
    return public_keys,encrypted

def RSA_Decrypt(private_key, encrypted):
    n, d = private_key
    decrypted = []
    encrypted = encrypted.replace("[","")
    encrypted = encrypted.replace("]","")
    encrypted = encrypted.split(",")
    encrypted = [int(i) for i in encrypted]
    for char in encrypted:
        decrypted.append(chr((char ** d) % n))
    return ''.join(decrypted)
    