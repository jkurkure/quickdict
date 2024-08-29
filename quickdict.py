from nltk.corpus import brown
import sys, os

from rich.progress import track
from nltk.corpus import wordnet as wn

# find = lambda w: set([word for word in brown.words() if w == word[:len(w)] ])
dictry = []
for word in track(brown.words(), description="Loading dictionary"):
	if word not in dictry:
		dictry.append(word)

def find(w, reverse=False):
	for word in dictry:
		if (w == word[:len(w)] and not reverse) or (w == word[-len(w):] and reverse):
			yield word


if __name__ == "__main__":
	results = find(sys.argv[1], reverse = sys.argv[-1]=='-r')

	if len(sys.argv) > 2:
		results = (r for r in results if len(r) >= eval(sys.argv[2]))
	
	f = open('out.tmp', 'w')
	sys.stdout = f
	for r in track(results, description="Looking up words"):
		defns = wn.synsets(r)
		print(r)
		for d in defns:
			print("\t", wn.synset(d.name()).definition()) # type: ignore

	os.system('less out.tmp')
	f.close()
	os.remove('out.tmp')