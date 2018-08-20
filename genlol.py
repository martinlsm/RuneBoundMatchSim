x = 0
n = 2

def gen():
	global x
	global n
	while x < n:
		x += 1
		yield 'Nope'
	else:
		yield 'Yep'

itr = gen()

print(next(itr))
print(next(itr))
print(next(itr))
print(next(itr))
