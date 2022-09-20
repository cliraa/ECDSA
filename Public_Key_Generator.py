import random

'''

This code was made for the purpose of creating an executable file (.exe) 
that generates public keys using elliptic curve cryptography (ECC).
This is done by introducing private keys in a mathematical function.

The user can type a private key of his choice (in decimal or hexadecimal form), 
or the program can assign one through a pseudo-random number.

How useful is this code? With it, the user will be able to create public keys without 
the need to be connected to the Internet, and that is very interesting because of issues 
related to computer security.

I would like to clarify that the code is not entirely mine. 
The study of the application of elliptic curves in cryptography has already some 
decades of development and there is plenty of (open source) code related to these advances.
Many of them, it seems, take this code as a reference: 
https://github.com/wobine/blackboard101/blob/master/EllipticCurvesPart4-PrivateKeyToPublicKey.py

My job has been to study it to adapt it to my requirements (put it all together in a single 
executable file) to learn, experiment and share how this interesting mathematical base is applied.

The public key generator, using the Elliptic Curve Digital Signature Algorithm (ECDSA), 
is presented below:

'''

# Elliptic Curve parameters (secp256k1)

Pcurve = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 -1
Acurve = 0
Bcurve = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
GPoint = (int(Gx),int(Gy)) # Generator point.
N=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

question = input("Do you want to type your Private Key? (Type 'Yes' or 'No'): ")

if question == "Yes":
    print(" ")
    print("Ok, perfect!")
    print(" ")
    question2 = input("To type the private key in decimal form, type 'D'; to type it in HexForm type 'H'?: ")
    if question2 == "D":
        print(" ")
        question3 = input("What is the Private Key?: ")
        privKey = int(question3)
        print(" ")
        print("Your Private Key in decimal form is: " + str(privKey))
    else:
        print(" ")
        question4 = input("Type your Private Key (in HexForm): ")
        privKey = int(question4, 16)
        print(" ")
        print("Your Private Key in decimal form is: " + str(privKey))

else:
    print(" ")
    print("Your Private Key (in decimal form) will be:")
    print(" ")
    lmt = 2 ** 252
    privKey = random.randrange(lmt, N)
    print(privKey)
    HexprivKey = hex(privKey)
    print(" ")
    print("Your Private Key in HexForm will be:")
    print(" ")
    print(HexprivKey)

def modinv(a,n=Pcurve): # Extended Euclidean Algorithm
    lm, hm = 1,0
    low, high = a%n,n
    while low > 1:
        ratio = high//low
        nm, new = hm-lm*ratio, high-low*ratio
        lm, low, hm, high = nm, new, lm, low
    return lm % n

def ECadd(a,b): # EC Addition
    LamAdd = ((b[1]-a[1]) * modinv(b[0]-a[0],Pcurve)) % Pcurve
    x = (LamAdd*LamAdd-a[0]-b[0]) % Pcurve
    y = (LamAdd*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def ECdouble(a): # EC Doubling
    Lam = ((3*a[0]*a[0]+Acurve) * modinv((2*a[1]),Pcurve)) % Pcurve
    x = (Lam*Lam-2*a[0]) % Pcurve
    y = (Lam*(a[0]-x)-a[1]) % Pcurve
    return (x,y)

def EccMultiply(GenPoint,ScalarHex): # Doubling & Addition
    if ScalarHex == 0 or ScalarHex >= N: raise Exception("Invalid Scalar/Private Key")
    ScalarBin = str(bin(ScalarHex))[2:]
    Q=GenPoint
    for i in range (1, len(ScalarBin)):
        Q=ECdouble(Q)
        if ScalarBin[i] == "1":
            Q=ECadd(Q,GenPoint)
    return (Q)

PublicKey = EccMultiply(GPoint,privKey)

XPublicKey = PublicKey[0]
YPublicKey = PublicKey[1]

print(" ")
print("The Public Key (in decimal form) is: ")
print(" ")
print("XCoor is: " + str(XPublicKey))
print("YCoor is: " + str(YPublicKey))

HexXPublicKey = hex(XPublicKey)
HexYPublicKey = hex(YPublicKey)

print(" ")
print("In HexForm:")
print(" ")
print("XCoor is: " + str(HexXPublicKey))
print("YCoor is: " + str(HexYPublicKey))

print(" ")
bye = input("Type anything to Exit")