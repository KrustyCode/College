from mod_inverse import mod_inverse
import secrets

class Curve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

class Point:
    #y^2 = x^3 + ax + b 
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def is_on_curve(self):
        lhs = (self.y**2) % self.curve.p
        rhs = (self.x**3 + self.curve.a * self.x + self.curve.b) % self.curve.p
        return round (lhs, 6) == round (rhs, 6)
    
    def __repr__(self):
        if self.x is None or self.y is None:
            return "Point(Identity)"
        return f"Point(x={hex(self.x)}, y={hex(self.y)})"
    
    def __add__(self, other):
        #two points are inverse of each other
        if not self.is_on_curve() or not other.is_on_curve():
            raise TypeError ('The points are not not curve')
        
        if not isinstance(self, Point) or not isinstance(other, Point):
            raise TypeError ('Expected objects of class Point')
        
        if self.x == None:
            return other
        if other.x == None:
            return self

        if self.x == other.x and self.y  == -(other.y - self.curve.p):
            return Point(x = None, y = None, curve = self.curve)
        
        #two points are different
        if self.x != other.x:
            m = (other.y - self.y) * mod_inverse(other.x - self.x, self.curve.p)

        
        #two points are the same or point doubling (derivative)
        if self.x == other.x and self.y == other.y:
            m = (3*self.x**2 + self.curve.a) * mod_inverse(2*self.y, self.curve.p)

        x3 = (m**2 - self.x - other.x) % self.curve.p
        y3 = (-(m*(x3 - self.x) + self.y)) % self.curve.p
        return Point(x = x3, y = y3, curve = self.curve)
    
    def __mul__(self, other):
        track = [(1, self)]
        while track[-1][0] + track[-1][0] < other:
            track.append ((track[-1][0] + track[-1][0], track[-1][1] + track[-1][1]))

        for tracker, result in reversed(track):
            if track[-1][0] + tracker <= other:
                track.append ((track[-1][0] + tracker, track[-1][1] + result))
        
        return track[-1][1]



elliptic_curve = Curve (
    a = 0,
    b = 7,
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
)

G_Point = Point (
    x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    curve = elliptic_curve
)

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBAAEDCE6AF48A03BBFD25E8CD0364141

def encrypt (message, public_key):
    temp_random_key = secrets.randbelow(n - 1) + 1
    C1 = G_Point * temp_random_key
    shared_secret = public_key * temp_random_key
    C2 = (message * shared_secret.x) % elliptic_curve.p 
    return C1, C2

def decrypt(C1, C2, private_key):
    shared_secret = C1 * private_key  # PrivateKey * C1
    message = (C2 * mod_inverse(shared_secret.x, elliptic_curve.p)) % elliptic_curve.p  # C2 dibagi shared_secret
    return message

message = 123456789


if __name__ == "__main__":
    # print(G_Point.is_on_curve())
    # g3 = G_Point * 5  
    # print(g3.x, g3.y)
    private_key = secrets.randbelow(n)

    # print(f'Private Key: {hex(private_key)}')

    public_key = G_Point * private_key
    # print(f'\nPublic key: {hex(public_key.x), hex(public_key.y)}')

    print(f'Original Message: {message}')
    C1, C2 = encrypt(message, public_key)

    print(f"Ciphertext: (C1={C1}, C2={C2})")

    decrypted_message = decrypt(C1, C2, private_key)
    print(f"Decrypted Message: {decrypted_message}")
