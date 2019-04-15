#!/usr/bin/env python

from ConceptMatcher import ConceptMatcher
import unittest,time, pstats,requests,cProfile

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n----------Loading Concepts--------------\n")
        with open("data/sample-concepts-1.txt","r", encoding="utf-8-sig") as f:
            cls.small_concept_matcher = ConceptMatcher(set(line.lower().rstrip() for line in f),3)
        with requests.get("http://www.mieliestronk.com/corncob_lowercase.txt","r") as f:
            cls.web_concepts_matcher = ConceptMatcher(set(f.text.split('\r\n')),4)
        print("web_concepts_matcher.max_tokens: ",cls.web_concepts_matcher.max_tokens)
        print("ConceptMatcher.max_tokens; ",ConceptMatcher.max_tokens)
        with open("data/sample-utterances-1.txt","r", encoding="utf-8-sig") as f:
            cls.test_utterances = list(line for line in f)
        print("\n----------Loaded--------------\n")
        cls.pr = cProfile.Profile()
        
    def setUp(self):
        self.startTime = time.time()
        if not self.id() == '__main__.Tests.test_4':
            self.pr.enable()
    
    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t))
        self.pr.disable()
        pstats.Stats(self.pr).print_stats()
        print("\n--------------------------------------\n")
    
    def test_1(self):
        correctResults = [{'thai'}, {'sushi'}, None, {'east asian'}, {'west indian', 'indian'},None]
        for i,utterance in enumerate(self.test_utterances):
            self.assertEqual(self.small_concept_matcher.return_matching_concepts(utterance), correctResults[i])
        print(f'\n Match on {len(self.small_concept_matcher.concepts)} Concepts\n')
    
    def test_2(self):
        correctResults = [{'like', 'some', 'thai', 'would','food'},
                          {'can', 'find', 'good', 'where','sushi'},
                          {'does', 'find', 'me', 'place', 'that','tapas'},
                          {'asian', 'do', 'east', 'restaurants', 'which','food'},
                          {'do', 'indian', 'restaurants', 'west', 'which','food'},
                          {'is', 'like', 'the', 'weather', 'what','today'}]
        for i,utterance in enumerate(self.test_utterances):
            self.assertEqual(self.web_concepts_matcher.return_matching_concepts(utterance), correctResults[i])
        print(f'\n Match on {len(self.web_concepts_matcher.concepts)} Concepts\n')
    
    def test_3(self):
        correctResult = {'do east asian',
            'which',
            'restaurants do',
            'do east',
            'do',
            'east',
            'which restaurants do',
            'restaurants',
            'restaurants do east',
            'east asian',
            'which restaurants',
            'asian',
            'asian food',
            'east asian food',
            'food',
            'to know',
            'to know which',
            'want to',
            'i',
            'want',
            'know which restaurants',
            'want to know',
            'know which',
            'to',
            'i want',
            'i want to',
            'know',
            'k',
            'asian food k',
            'food k',}
        self.assertEqual(ConceptMatcher._cut_utterance('I want to know which restaurants do East Asian Food, k?',3), correctResult)
        
    def test_4(self):
        with requests.get("https://algs4.cs.princeton.edu/63suffix/mobydick.txt","r") as f:
            self.pr.enable()
            self.web_concepts_matcher.batch_utterances(f)
        self.web_concepts_matcher.process_utterance_list()
        print(f'{self.web_concepts_matcher.num_matches} matches in Moby Dick with {self.web_concepts_matcher.num_inputs_processed} input strings')
        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=0).run(suite)