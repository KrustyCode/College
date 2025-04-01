import random

# Parameter Kurva Eliptik (y^2 = x^3 + ax + b mod p)
p = 0xfffffffffffffffffffffffffffffffeffffffffffffffff  # Prime field
a = -3
b = 0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875a
G = (  # Titik generator (Gx, Gy)
    0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    0x4fe342e2fe1a7f9bb79eac49ba3dfc5cbe4d62b64b7797bc9f8ae0f1976bde64,
)
n = 0xffffffffffffffffffffffff99def836146bc9b1b4d22831  # Order dari G

# Fungsi operasi titik ECC
def ecc_add(P, Q, p):
    """Tambah dua titik P dan Q di kurva eliptik"""
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q

    if P == Q:  # Jika titik sama, gunakan formula slope untuk doubling
        lambd = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p
    else:  # Jika titik berbeda
        lambd = (y2 - y1) * pow(x2 - x1, -1, p) % p

    x3 = (lambd**2 - x1 - x2) % p
    y3 = (lambd * (x1 - x3) - y1) % p
    return x3, y3

def ecc_mul(k, P, p):
    """Perkalian skalar: k * P menggunakan metode double-and-add"""
    R = None
    Q = P
    while k:
        if k & 1:
            R = ecc_add(R, Q, p)
        Q = ecc_add(Q, Q, p)
        k >>= 1
    return R

# Generate Private Key dan Public Key
private_key = random.randint(1, n - 1)
public_key = ecc_mul(private_key, G, p)

print(f"Private Key: {hex(private_key)}")
print(f"Public Key: {public_key}")

# Enkripsi menggunakan ECC ElGamal
def encrypt(message, public_key):
    """Enkripsi message sebagai integer menggunakan public key"""
    k = random.randint(1, n - 1)
    C1 = ecc_mul(k, G, p)  # k * G
    shared_secret = ecc_mul(k, public_key, p)  # k * PublicKey
    C2 = (message * shared_secret[0]) % p  # Pesan dikali shared_secret
    return C1, C2

def decrypt(C1, C2, private_key):
    """Dekripsi ciphertext"""
    shared_secret = ecc_mul(private_key, C1, p)  # PrivateKey * C1
    message = (C2 * pow(shared_secret[0], -1, p)) % p  # C2 dibagi shared_secret
    return message

# Contoh Enkripsi & Dekripsi
message = "I Love You"  # Pesan dalam bentuk integer
C1, C2 = encrypt(message, public_key)
print(f"Ciphertext: (C1={C1}, C2={C2})")

decrypted_message = decrypt(C1, C2, private_key)
print(f"Decrypted Message: {decrypted_message}")
