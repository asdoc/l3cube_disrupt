from random import randrange as rr

def experiment(N):
	cnt = [0 for i in xrange(365)]
	for i in xrange(N):
		cnt[rr(365)] += 1
	for x in cnt:
		if x > 1:
			return 1
	return 0

def main():
	TRIALS = int(raw_input('Enter the number of trials to be performed: '))
	N = int(raw_input('Enter the number of people: '))
	success = 0
	for i in xrange(TRIALS):
		if experiment(N):
			success += 1
	print 'Total number of experiments having at least one pair with the same birthday: {0}'.format(success)
	print 'Probability of at least 1 pair of people having the same bithday = {0}'.format(float(success)/TRIALS)

if __name__ == '__main__':
	main()
