import json, sys
import base64
from Datum import Datum

class FeatureFactory:
    """
    Add any necessary initialization steps for your features here
    Using this constructor is optional. Depending on your
    features, you may not need to intialize anything.
    """
    def __init__(self):
        pass


    """
    Words is a list of the words in the entire corpus, previousLabel is the label
    for position-1 (or O if it's the start of a new sentence), and position
    is the word you are adding features for. PreviousLabel must be the
    only label that is visible to this method. 
    """


    def computeFeatures(self, words, previousLabel, position):
        features = []
        currentWord = words[position]

        """ Baseline Features """
        features.append("word=" + currentWord)
        features.append("prevLabel=" + previousLabel)
        features.append("word=" + currentWord + ", prevLabel=" + previousLabel)
	"""
        Warning: If you encounter "line search failure" error when
        running the program, considering putting the baseline features
	back. It occurs when the features are too sparse. Once you have
        added enough features, take out the features that you don't need. 
	"""
        
        """ TODO: Add your features here """
        # Name Entity Examples :
        '''
        Justin
        R'Hanks
        Justin Hanks
        Hanks said
        Justin-Hanks
        Justin var Hanks
        '''
        # last char 
        if currentWord[-1] in 'aeiou':
            features.append('endwith_vowel')
            features.append('endwith_vowel, prevLabel=' + previousLabel)
        elif currentWord[-1] == 's':
            features.append('endwith_s')
        elif currentWord[-1] == 'r':
            features.append('endwith_r')

        # last two char 
        if currentWord[-2:] == 'ed':
            features.append('endwith_ed')
        elif currentWord[-2:] == 'es':
            features.append('endwith_es')
        # last three char 
        if currentWord[-3:] == 'nia':
            features.append('endwith_nia')
        elif currentWord[-3:] == 'ian':
            features.append('endwith_ian')
        elif currentWord[-3:] == 'nal':
            features.append('endwith_nal')
        elif currentWord[-3:] == 'ing':
            features.append('endwith_ing')
        elif currentWord[-3:] == 'ies':
            features.append('endwith_ies')
        elif currentWord[-3:] == 'day':
            features.append('endwith_day')
        elif currentWord[-3:] == 'ity':
            features.append('endwith_ity')
        elif currentWord[-3:] == 'ive':
            features.append('endwith_ive')
        elif currentWord[-3:] == 'ent':
            features.append('endwith_ent')
        elif currentWord[-3:] == 'ese':
            features.append('endwith_ese')
        elif currentWord[-3:] == 'ish':
            features.append('endwith_ish')
        # last four char 
        if currentWord[-4:] == 'stan':
            features.append('endwith_stan')
        elif currentWord[-4:] == 'sion':
            features.append('endwith_sion')
        elif currentWord[-4:] == 'tion':
            features.append('endwith_tion')
        elif currentWord[-4:] == 'land':
            features.append('endwith_land')
        elif currentWord[-4:] == 'bury':
            features.append('endwith_bury')
      
        # 
        has_digit = False 
        has_punctuation = False

        capList = []
        for i in range( len(currentWord) ):
            if (currentWord[i].isupper()):
                capList.append(i)
            if currentWord[i] in "-.,=';:?" and not has_punctuation:
                has_puctuation = True
            if currentWord[i].isdigit() and not has_digit:
                has_digit = True
        
        if has_digit:
            features.append('has_digit')
        if has_punctuation :
            features.append('has_punctuation')

        if len(capList) == 0:
            features.append('case_lowercase')
        elif len(capList) == 1 and capList[0] == 0:
            features.append('case_Title')
            features.append('prevLabel=' + previousLabel + ', case_Title')
        elif len(capList) == len(currentWord):
            features.append('case_AllCap')
        elif len(capList) < len(currentWord) and len(capList) > 1:
            features.append('case_Camel')
            features.append('prevLabel=' + previousLabel + ', case_Title')
        
        
        return features

    """ Do not modify this method """
    def readData(self, filename):
        data = [] 
        
        for line in open(filename, 'r'):
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data

    """ Do not modify this method """
    def readTestData(self, ch_aux):
        data = [] 
        
        for line in ch_aux.splitlines():
            line_split = line.split()
            # remove emtpy lines
            if len(line_split) < 2:
                continue
            word = line_split[0]
            label = line_split[1]

            datum = Datum(word, label)
            data.append(datum)

        return data


    """ Do not modify this method """
    def setFeaturesTrain(self, data):
        newData = []
        words = []

        for datum in data:
            words.append(datum.word)

        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        previousLabel = "O"
        for i in range(0, len(data)):
            datum = data[i]

            newDatum = Datum(datum.word, datum.label)
            newDatum.features = self.computeFeatures(words, previousLabel, i)
            newDatum.previousLabel = previousLabel
            newData.append(newDatum)

            previousLabel = datum.label

        return newData

    """
    Compute the features for all possible previous labels
    for Viterbi algorithm. Do not modify this method
    """
    def setFeaturesTest(self, data):
        newData = []
        words = []
        labels = []
        labelIndex = {}

        for datum in data:
            words.append(datum.word)
            if not labelIndex.has_key(datum.label):
                labelIndex[datum.label] = len(labels)
                labels.append(datum.label)
        
        ## This is so that the feature factory code doesn't
        ## accidentally use the true label info
        for i in range(0, len(data)):
            datum = data[i]

            if i == 0:
                previousLabel = "O"
                datum.features = self.computeFeatures(words, previousLabel, i)

                newDatum = Datum(datum.word, datum.label)
                newDatum.features = self.computeFeatures(words, previousLabel, i)
                newDatum.previousLabel = previousLabel
                newData.append(newDatum)
            
            else:
                for previousLabel in labels:
                    datum.features = self.computeFeatures(words, previousLabel, i)
                    newDatum = Datum(datum.word, datum.label)
                    newDatum.features = self.computeFeatures(words, previousLabel, i)
                    newDatum.previousLabel = previousLabel
                    newData.append(newDatum)

        return newData

    """
    write words, labels, and features into a json file
    Do not modify this method
    """
    def writeData(self, data, filename):
        outFile = open(filename + '.json', 'w')
        for i in range(0, len(data)):
            datum = data[i]
            jsonObj = {}
            jsonObj['_label'] = datum.label
            jsonObj['_word']= base64.b64encode(datum.word)
            jsonObj['_prevLabel'] = datum.previousLabel

            featureObj = {}
            features = datum.features
            for j in range(0, len(features)):
                feature = features[j]
                featureObj['_'+feature] = feature
            jsonObj['_features'] = featureObj
            
            outFile.write(json.dumps(jsonObj) + '\n')
            
        outFile.close()

