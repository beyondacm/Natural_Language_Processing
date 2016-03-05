import sys
import os
import re
import pprint

#my_first_pat = '(\w+\.\w+|\w+)[ ]*(@| at | AT |&#x40;)[ ]*(\w+\.\w+|\w+).(edu|com|EDU)'
email_pattern = '(\w+\.\w+|\w+)[ ]*(@| at | AT |&#x40;)[ ]*(\w+|\w+\.\w+).(edu|com|EDU)'
ep = re.compile(email_pattern)
phone_pattern = '(\d{3})(\D){1,3}(\d{3})(-| )(\d{4})'
pp = re.compile(phone_pattern)


"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    res = []
    for line in f:
        #line.replace(' at ', '@')
        line = line.replace(' dot ', '.')
        line = line.replace(' dt ', '.')
        line = line.replace(';', '.')
        #matches = re.findall(my_first_pat,line)
        email_matches = ep.search(line)
        phone_matches = pp.findall(line)
        #print phone_matches
        if email_matches :
            #print matches.group(1), matches.group(3)
            #for m in matches:
            email_group1 = email_matches.group(1)
            email_group3 = email_matches.group(3)
            email_group4 = email_matches.group(4)
            email = '%s@%s.%s' % ( email_group1 , email_group3, email_group4 )
            #print name , email
            res.append((name,'e',email))
        if phone_matches : 
            #print phone_matches
            for m in phone_matches :
                #print m[1], m[3], m[4]
                phone = '%s-%s-%s' %(m[0], m[2], m[4])
                print name, phone
                res.append((name, 'p', phone))
            
            #phone = '%s-%s-%s' %(phone_group2, phone_group4, phone_group5)
            #res.append((name, 'p', phone))

        #print matches
        #matches = email_pattern.findall(line) 
        #print matches
        #for m in matches:
            #print m  #m is a tuple 
            #email = '%s@%s.edu' % m
            #res.append((name,'e',email))
    #print res
    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    # print os.listdir(data_path)
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        #print path
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        #print f_guesses
        guess_list.extend(f_guesses)
    # print guess_list
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) == 1):
        main('../data/dev', '../data/devGOLD')
    elif (len(sys.argv) == 3):
        main(sys.argv[1],sys.argv[2])
    else:
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
