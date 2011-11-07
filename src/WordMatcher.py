from __future__ import division
from xml.etree.cElementTree import iterparse
import Pair as p
import ResultPrinter as rp
import eval_rte

class WordMatcher:
	threshHold = 0.4
	result = -1
	pairs = {}

	def __init__(self, inf):#t, h, idx):
		currentPair = p.Pair()
		currentID = 0
		for event, elem in iterparse(inf):
			if elem.tag == "t":
				currentPair.text = elem.text.lower().split(" ")
			if elem.tag == "h":
				currentPair.hypothesis = elem.text.lower().split(" ")
			if elem.tag == "pair":
				print elem.get("id")
				#print "in init: ", currentPair.text, ", ", currentPair.result, ", ", currentPair.hypothesis 
				self.pairs[int(elem.get("id"))] = currentPair
				currentPair = p.Pair()
		
	def match(self, i): # i is id of pair
		return self.simpleMatch(i)
		
	def simpleMatch(self, i): # i is id of pair
		occ = 0
		currentPair = self.pairs[i]
		for word in currentPair.hypothesis:
			if word in currentPair.text:
				occ +=1
		#print "occ: ", occ, "len: ", len(currentPair.hypothesis)
		currentPair.result = occ/len(currentPair.hypothesis)
	
	def isGood(self, i): # i is id of pair
		currentPair = self.pairs[i]
		if currentPair.result < 0:
			self.match(i)
		return "YES" if currentPair.result >= self.threshHold else "NO"
		
	def verbose(self, i): #i is id of pair
		#print "in verbose: ", self.pairs[i].text, ", ", self.pairs[i].result, ", ", self.pairs[i].hypothesis 
		if self.pairs[i].result < 0:
			self.match(i)
		#print "%.2f" % (self.pairs[i].result*100), "% is a", self.isGood(i)


#test
wordtest = WordMatcher("../data/RTE2_dev.xml")
resultP = rp.ResultPrinter()
for i in range(1, len(wordtest.pairs)+1):
	print i
	wordtest.verbose(i)
	resultP.write(i, wordtest.isGood(i))

	
	