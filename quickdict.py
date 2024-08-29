import sys, os

while True:
	try:
		from nltk.corpus import brown
		from rich.progress import track
		from nltk.corpus import wordnet as wn
		break
	except ModuleNotFoundError:
		os.system("pip install nltk rich")
		continue

# find = lambda w: set([word for word in brown.words() if w == word[:len(w)] ])
dictry = []
while True:
	try:
		for word in track(brown.words(), description="Loading dictionary"):
			if word not in dictry:
				dictry.append(word)
		break
	except LookupError:
		import nltk
		nltk.download("brown")
		continue

def find(w, reverse=False):
	for word in dictry:
		if (w == word[:len(w)] and not reverse) or (w == word[-len(w):] and reverse):
			yield word


if __name__ == "__main__":
	results = find(sys.argv[1], reverse = sys.argv[-1]=='-r')

	if len(sys.argv) > 2:
		results = (r for r in results if len(r) >= eval(sys.argv[2]))
	
	f = open('out.tmp', 'w')
	for r in track(results, description="Looking up words"):
		while True:
			try:
				defns = wn.synsets(r)
				break
			except LookupError:
				import nltk
				nltk.download("wordnet")
				continue

		print(r, file=f)
		for d in defns:
			print("\t", wn.synset(d.name()).definition(), file=f)

	os.system('less out.tmp')
	f.close()
	os.remove('out.tmp')