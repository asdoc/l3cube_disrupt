from random import randrange as rr

# Function to simulate random experiment.
# 'N' people are assigned a random birthday from 365 days
# If >= 2 people have the same birth date, 
#     function returns True
# Else, function returns False

def experiment(N):
	birthdates = [0 for i in xrange(365)]
	for i in xrange(N):
		birthdates[rr(365)] += 1
	for count_birthdate in birthdates:
		if count_birthdate > 1:
			return True
	return False

# Probability of at least 2 people having the same birthday is found out using random experiments.
# P(B) = P(A) / P(S), where:
#        P(A) = Number of experiments in which at least 2 people have the same birthday
#        P(S) = Total number of experiments

def main():
	try:
		TRIALS = int(raw_input('Enter the number of trials to be performed: '))
	except ValueError as e:
		TRIALS = 10000 # Default number of trials
	try:
		NUM_PEOPLE = int(raw_input('Enter the number of people: '))
	except ValueError as e:
		NUM_PEOPLE = 23 # Default number of people for which trials will be performed

	success = 0
	for i in xrange(TRIALS):
		if experiment(NUM_PEOPLE):
			success += 1

	print 'Total number of experiments having at least one pair with the same birthday: {0}'.format(success)
	print 'Probability of at least 1 pair of people having the same bithday = {0}'.format(float(success)/TRIALS)

if __name__ == '__main__':
	main()
