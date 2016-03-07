import collections, math

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # TODO your code here
    
    self.laplaceUniGramCounts = collections.defaultdict(lambda : 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
        #print sentence
        for datum in sentence.data:
            #print 'datum :' + str(datum)    # datum includes the (correct, non-correct)
            token = datum.word              # token is the correct word
            #print 'token :' + str(token)
            self.laplaceUniGramCounts[token] = self.laplaceUniGramCounts[token] + 1
            self.total += 1
            #print token, self.laplaceUniGramCounts[token], self.total
    #print self.laplaceUniGramCounts
    #print self.total
    #print len(self.laplaceUniGramCounts)
    pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    
    score = 0
    # Use the Laplace smoothing / add-one estimation
    # Add-1 estimate : 1. Pretend we saw each word one more time thant we did
    #                  2. Just add one to all the counts / V / len(laplaceUniGramCounts)
    for token in sentence :
        count = self.laplaceUniGramCounts[token]
        score += math.log(count+1)
        score -= math.log(self.total + len(self.laplaceUniGramCounts))
    return score
    #return 0.0
