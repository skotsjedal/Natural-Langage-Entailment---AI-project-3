from xml.etree.cElementTree import iterparse

class FileReader:
	fields = ["word", "lemma", "pos-tag"]	

	def __init__(self, inf, abstract = True):
		self.elems = {}
		self.pairs = 0

		cid = 0
		skip = False
		sentence = []
		attr = {}
		for event, elem in iterparse(inf, events=("start", "end")):

			if event == "start":
				if elem.tag == "pair":
					self.pairs+=1
					cid = elem.get("id")
					self.elems[cid] = []
				elif elem.tag == "node":
					if elem.get("id")[0] == "E" and not abstract:
						skip = True
					attr = {}
				elif elem.tag == "text" or elem.tag == "hypothesis":
					sentence = []
				elif elem.tag == "sentence":
					sid = "X"+str(elem.get("serial"))
				
			if event == "end":
				
				if elem.tag == "text" or elem.tag == "hypothesis":
					self.elems[cid].append(sentence)
				elif elem.tag == "node":
					if skip:
						skip = False
					else:
						attr["id"] = elem.get("id")+sid
						sentence.append(attr)
				elif elem.tag == "relation":
					attr["parent"] = elem.get("parent")+sid
					attr[elem.tag] = elem.text.strip("\n\t")
				elif elem.tag in self.fields and not skip:
					attr[elem.tag] = elem.text.strip("\n\t")
					
