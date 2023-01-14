# Recursion: when a function calls itself.
# https://youtube.com/shorts/k7ATqT1BK1g?feature=share
# here, for every number starting at 6, is multiplied by every number
#   underneath it until it reaches 1. so: 6!=6*5*4*3*2*1
#   6*5 = 30*4 = 120*3 = 360*2 = 720

def factorial(n):
    if n == 1: return 1
    return n * factorial(n-1)

print(factorial(6))
