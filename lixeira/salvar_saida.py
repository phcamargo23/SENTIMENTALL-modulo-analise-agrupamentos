import sys
with open('goat.txt', 'w') as f:
    sys.stdout = f
    print "test"