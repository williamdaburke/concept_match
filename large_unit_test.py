#!/usr/bin/env python

from ConceptMatcher import ConceptMatcher
from io import BytesIO
import unittest,time, pstats,requests,cProfile, gzip, urllib.request

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n -------Loading Wiki Dump-------\n\n This may take a minute... \n")
        request = urllib.request.Request('http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-all-titles-in-ns0.gz',headers={"Accept-Encoding": "gzip",})
        with urllib.request.urlopen(request) as response:
            deflatedContent = gzip.GzipFile(fileobj=BytesIO(response.read()))
        print("\n ----------Decoding Dump-------------- \n")
        cls.wiki_concepts_matcher = ConceptMatcher(deflatedContent.readlines(),4,processConcepts=True)
        del deflatedContent
        with open("data/sample-utterances-1.txt","r", encoding="utf-8-sig") as f:
            cls.test_utterances = list(line.rstrip() for line in f)
        print("\n----------Loaded--------------\n")
        cls.pr = cProfile.Profile()
    
    def setUp(self):
        self.startTime = time.time()
        if not self.id() in ['__main__.Tests.test_3','__main__.Tests.test_4']:
            self.pr.enable()
        
    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))
        self.pr.disable()
        pstats.Stats(self.pr).print_stats()
        print("\n--------------------------------------\n")
    
    def test_1(self):
        correctResults = [{'i', 'like', 'i would', 'thai', 'would', 'i would like', 'some','food','thai food'},
                          {'find', 'i', 'can', 'can i', 'where', 'good','sushi'},  
                          {'find', 'me', 'a', 'that', 'find me', 'does', 'place','tapas','me a'},
                          {'which', 'restaurants', 'east asian', 'east', 'do', 'asian','food','asian food'},
                          {'which', 'do', 'restaurants', 'indian', 'west', 'west indian','food','indian food'},
                          {'the', 'weather', 'is', 'like', 'what', 'the weather','what is','today'}]
        for i,utterance in enumerate(self.test_utterances):
            self.assertEqual(self.wiki_concepts_matcher.return_matching_concepts(utterance), correctResults[i])
        print(f'\n Match on {len(self.wiki_concepts_matcher.concepts)} Concepts\n')

    def test_2(self):
        with open("data/kangaroo.txt","r", encoding="utf-8-sig") as f:
            self.wiki_concepts_matcher.batch_utterances(f)
        self.wiki_concepts_matcher.process_utterance_list()
        
        print(f"+++++ {len(self.wiki_concepts_matcher.utterance_list)} +++++\n")
        print(f"+++++++++++++++ {len(self.wiki_concepts_matcher.concepts)} +++++\n")
        print(f"+++++++++++++++ {self.wiki_concepts_matcher.num_matches} +++++")
        print(f"+++++ {self.wiki_concepts_matcher.num_inputs_processed} +++++\n")
        
        with open("data/kangaroo_concepts.txt","r", encoding="utf-8-sig") as f:
            self.assertEqual(ConceptMatcher(set(line.rstrip() for line in f),4,True).concepts, self.wiki_concepts_matcher.matches)  
        
    def test_3(self):
        with requests.get("https://norvig.com/big.txt","r") as f:
            self.pr.enable()
            self.wiki_concepts_matcher.batch_utterances(f)
        self.wiki_concepts_matcher.process_utterance_list()
        print(f'{self.wiki_concepts_matcher.num_matches} matches in Adventures of Sherlock Holmes with {self.wiki_concepts_matcher.num_inputs_processed} input strings')
        
    def test_4(self):
        with requests.get("https://algs4.cs.princeton.edu/63suffix/mobydick.txt","r") as f:
            self.pr.enable()
            self.wiki_concepts_matcher.batch_utterances(f)
        self.wiki_concepts_matcher.process_utterance_list()
        print(f'{self.wiki_concepts_matcher.num_matches} matches in Moby Dick with {self.wiki_concepts_matcher.num_inputs_processed} input strings')
    
    def test_5(self):
        correctResults = {'asian',
                         'can',
                         'do',
                         'does',
                         'east',
                         'find',
                         'food',
                         'good',
                         'indian',
                         'is',
                         'like',
                         'me',
                         'place',
                         'restaurants',
                         'some',
                         'sushi',
                         'tapas',
                         'thai',
                         'that',
                         'the',
                         'today',
                         'weather',
                         'west',
                         'what',
                         'where',
                         'which',
                         'would',
                         'indian food',
                         'thai food',
                         'i',
                         'east asian',
                         'asian food',
                         'me a',
                         'i would',
                         'can i',
                         'the weather',
                         'a',
                         'west indian',
                         'find me',
                         'what is',
                         'i would like'}
        self.wiki_concepts_matcher.process_utterance_list(self.test_utterances)
        self.assertEqual(self.wiki_concepts_matcher.matches, correctResults)
        print(f'\n {self.wiki_concepts_matcher.num_matches} matches on {len(self.wiki_concepts_matcher.concepts)} Concepts\n')
    
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=0).run(suite)