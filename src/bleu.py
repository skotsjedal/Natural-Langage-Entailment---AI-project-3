from __future__ import division
import SentenceTree as st
import ResultPrinter as rp

class Bleu:

	thresh = 0.22

	result = {}
	
	def __init__(self):
		# False means exclude abstract nodes
		self.data = st.SentenceTree(False)

	def matchBleu(self):
		for n in range(1, 4+1):
			for i in range(1, self.data.pairs+1):
				self.data.setCurrentId(i)
				tBleu = self.data.getNGramText(n)
				hBleu = self.data.getNGramHyp(n)
				count = 0
				for b in hBleu:
					if b in tBleu:
						count += 1
				if n == 1:
				 	self.result[i] = count/len(hBleu)
				else:
					self.result[i] += count/len(hBleu)
		for key in self.result.keys():
			self.result[key] = "YES" if self.result[key]/4 > self.thresh else "NO"
		
	def printResults(self):
		if not self.result:
			self.matchBleu()
		printer = rp.ResultPrinter()
		for key in self.result.keys():
			printer.write(key, self.result[key])
			
b = Bleu()
b.printResults()

