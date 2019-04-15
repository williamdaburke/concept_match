#!/usr/bin/env python

class ConceptMatcher(object):
    def __init__(self,concepts,maxTokenMatch=None,processConcepts=False):
        #by default matches concepts of 3 words
        self.__concepts = set([self._preprocess_text(concept) for concept in concepts]) if processConcepts else concepts  
        if maxTokenMatch:
            self.max_tokens = maxTokenMatch
        self._clear_results()
    
    max_tokens = 3
    utterance_list = []
    
    __BYTES_TABLE = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f                0123456789       ABCDEFGHIJKLMNOPQRSTUVWXYZ      abcdefghijklmnopqrstuvwxyz    \x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'
    
    #replace '_' (95) with space (32) and remove other punctuation
    __STRING_TABLE = {95: 32, 33: None, 34: None, 35: None, 36: None, 37: None, 38: None, 9: None, 40: None, 41: None, 42: None, 43: None, 44: None, 45: None, 46: None, 47: None, 58: None, 59: None, 60: None, 61: None, 62: None, 63: None, 64: None, 91: None, 92: None, 93: None, 94: None, 96: None, 23: None, 124: None, 125: None, 126: None}
    
    @property
    def num_inputs_processed(self):
        return self.__num_processed_inputs
    
    @property
    def num_matches(self):
        return len(self.__concept_matches)
    
    @property
    def matches(self):
        return self.__concept_matches
    
    @property
    def concepts(self):
        return self.__concepts
    
    @staticmethod
    def _cut_utterance(input_string: str,maxtok=max_tokens):
        input_string = ConceptMatcher._preprocess_text(input_string)
        indices = [0]+[i for i, x in enumerate(input_string) if x == " "]+[len(input_string)]
        cuts = [input_string[:b] for b in indices[1:maxtok+1]]
        cuts += [input_string[indices[i]+1:b] for i in range(1,len(indices)-1) for b in indices[i+1:i+maxtok+1]]
        return set(cuts)
    
    @staticmethod
    def _preprocess_text(x):
        x = x.lower()
        if type(x) == bytes:
            return b' '.join(x.translate(ConceptMatcher.__BYTES_TABLE).split()).decode('utf-8')
        else:
            return ' '.join(x.translate(ConceptMatcher.__STRING_TABLE).split())
    
    def _clear_results(self):
        self.__num_processed_inputs = 0
        self.__concept_matches = set()
        
    def return_matching_concepts(self,input_string: str):
        #match token combinations of utterance with set of concepts
        res = self._cut_utterance(input_string,self.max_tokens).intersection(self.__concepts)
        self.__num_processed_inputs += 1
        return res if bool(res) else None
    
    def process_utterance_list(self,input_list=None):
        #match concept set to list of input strings
        self._clear_results()
        results =[]
        input_list = self.utterance_list if not input_list else input_list
        for utterance in input_list:
            match = self.return_matching_concepts(utterance)
            if match:
                results += match
        self.__concept_matches = self.__concept_matches.union(results)
        
    def batch_utterances(self,file,num_tokens=20):
        #utility for splitting longer text into small input strings
        text = ''.join([ConceptMatcher._preprocess_text(line) for line in file if line])
        spaces,char_start = 0,0
        text_length = len(text)-1
        for i in range(text_length):
            if i == text_length:
                self.utterance_list.append(text[char_start:i+1])  
            elif text[i] == ' ':
                spaces += 1
                if spaces == 20:
                    self.utterance_list.append(text[char_start:i])
                    char_start = i+1
                    spaces = 0