from scipy.stats import binom_test

test = binom_test(9, n=863, p=0.5, alternative='greater')

print(1 - test)
