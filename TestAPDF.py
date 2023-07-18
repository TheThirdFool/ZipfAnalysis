# This si a file to test a pdf for zipf

import PyPDF2
import sys
from matplotlib import pyplot as plt
from scipy import optimize as opt


# Declare a dictionary
dictionary = {}

def count(elements):
    # check if each word has '.' at its last. If so then ignore '.'
    if elements[-1] == '.':
        elements = elements[0:len(elements) - 1]
 
    # if there exists a key as "elements" then simply
    # increase its value.
    if elements in dictionary:
        dictionary[elements] += 1
 
    # if the dictionary does not have the key as "elements"
    # then create a key "elements" and assign its value to 1.
    else:
        dictionary.update({elements: 1})


def func(x, a, b, c):
#	a = params[0]
#	b = parmas[1]
#	c = params[2]
	y = c / (x + b)**a
	return y



#scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False, check_finite=None, bounds=(-inf, inf), method=None, jac=None, *, full_output=False, nan_policy=None, **kwargs)

def main():
	
	inFileName = sys.argv[1]

	# creating a pdf reader object
	reader = PyPDF2.PdfReader(inFileName)
	
	# print the number of pages in pdf file
	print("This pdf has ", (len(reader.pages)), " pages!")
	
	# print the text of the first page
	# getting a specific page from the pdf file
	pn = 0
	while(pn < len(reader.pages)):
		page = reader.pages[pn]
  
		# extracting text from page
		text = page.extract_text()
		wordList = text.split()
		for word in wordList:
			if not word.isalpha():
				continue
			count(word.lower());

		pn = pn + 1


	total = sum(dictionary.values())
	rank = 1

	x = []
	y = []

	for w in sorted(dictionary, key=dictionary.get, reverse=True):
		if(rank < 20):
			print(repr(w), dictionary[w])
		x.append(rank)
		y.append(dictionary[w] / total)
		rank = rank + 1

	plt.scatter(x, y, label="Data")
	plt.yscale('log')
	plt.xscale('log')

	# The actual curve fitting happens here
	optimizedParameters, pcov = opt.curve_fit(func, x, y);

	# Use the optimized parameters to plot the best fit
	plt.plot(x, func(x, *optimizedParameters), label="Fit", color="red");

	plt.title("Zipf analysis on " + inFileName)
	plt.xlabel("Word rank")
	plt.ylabel("Word frequency")
	plt.legend()
	plt.show()





	






main()


