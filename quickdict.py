import sys, os, platformdirs, pickle, time

while True:
	try:
		
		from rich.progress import track
		from nltk.corpus import brown
		from nltk.corpus import wordnet as wn
		break
	except ModuleNotFoundError:
		os.system("pip install nltk rich")
		continue

data_dir = platformdirs.user_data_dir(appname="quickdict", appauthor="jkurkure")
if not os.path.exists(data_dir):
	os.makedirs(data_dir)
file_path = os.path.join(data_dir, "day-archive.sav")

registry = {}

if os.path.exists(file_path):
	with open(file_path, "rb") as file:
		registry = pickle.load(file)

if "dict" not in registry:
	registry["dict"] = []
	while True:
		try:
			for word in track(brown.words(), description="Loading dictionary"):
				if word not in registry["dict"]:
					registry["dict"].append(word)
			break
		except LookupError:
			import nltk
			nltk.download("brown")
			continue

# find = lambda w: set([word for word in brown.words() if w == word[:len(w)] ])

def find(w, reverse=False):
	for word in registry["dict"]:
		if (w == word[:len(w)] and not reverse) or (w == word[-len(w):] and reverse):
			yield word


if __name__ == "__main__":
	id = " ".join([s for s in sys.argv[1:]])
	if id in registry:
		f = open('out.tmp', 'w')
		print(registry[id], file=f)
		f.close()
		if os.stat("out.tmp").st_size > 0:  
			os.system('less out.tmp')
		else:
			print("No matches found!")
		os.remove('out.tmp')
		exit()

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
			
	if os.stat("out.tmp").st_size > 0:  
		os.system('less out.tmp')
	else:
		print("No matches found!")
		
	f.close()
	with open('out.tmp', 'r') as f:
		registry[id] = f.read()
	os.remove('out.tmp')

	with open(file_path, "wb") as file:
		pickle.dump(registry, file)