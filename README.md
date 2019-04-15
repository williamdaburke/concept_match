This is a class to match input strings to concepts, as outlined in the Programming Assignment.

I have made a few assumptions, one being that the results did not need to be case sensitive. 
I could have returned matching cases for the results, by mapping concepts to their original values, but did not add
this to my solution.  I am assuming numbers are always in the same format between input string and concept, although,
this could have been converted if desired. I assume not deflections of differences in grammar or endings between
concepts and input as well.  In another excercise lemmatization could have been used to deal with this.  Another possible
issue is words with multiple meanings with match, even if meant to be different (to live vs. live music).  
(I also assume the ASR being used will know the difference between the two and write them correctly).  
Many of these issues could be handled with the help of word embeddings and other nlp frameworks outside of the 
standard pythong library, to which I have limited myself. 

The algorithm I have created has a worst case time complexity of O(len(t)*len(c)), where t is tokens in the input_string
and c is the set of concepts, based on the fact that a set could have to hashes collision if overloaded.  
However, in practice that would be very rare, even with millions of concepts, as seen in the 'large_unit_test' attached.
The time average complexity is O(min(len(t),len(c))) as seen in the profiling in the tests. This is a small number
since the number of tokens never exceeds 20, which is why I settled on this solution.

The calculation time for one input string of max 20 words is less than a millisecond, even with over 10 million concepts.
This latency increases if many input strings are given, as each must be cut into types of concepts, but I am assuming
only a limited amout of input strings need to be processed at one time.  Some processing could have been sped up with multiprocessing, however that seemd out of scope.

To run the unit test enter the command 'large_unit_test.py' or 'small_unit_test.py' from this directory.  
The code is meant for python3.

Some of the challenges included organizing internal properties to keep them seperate when multiple 
implementation of the class are used. To solve this I have attempted to create properties accessible only for 
the current instance of the class, while at the same time trying to minimize the need to pass self into methods
which can be static.

The algorithm is based on returning the intersection of two sets, which seemed more scalable for large concept lists.
I realize that this is a somewhat 'high-level' data structure, but it seems more efficient in python than using
a type of iterative search algorithm.  If I had more time I would have written it in a compiled language.

I have tried to increase speed by using "translate" with a custom translation table for strings and bytes rather than
regex of "replace".  Also, I was able to combine several replacements at once with these tables, two reduce
iterations through the strings. Also helpful for replacing '_' with space, as was necessary for the wiki dump used
in the large unit test. This means however, I always replace _ with space, which seems to make sense anyway.
have considered both strings and bytes, so that it is possible to preprocess any type of content.
Doing to the translation in bytes is faster than decoding to string first and translating after.

List comprehension has given faster results than for loops, therefore I have used it by preference, despite the
possible loss in readability. It has reduced the use of 'append'.

When creating sets I have made a list first and converted to set once it is ready, rather than adding to a set once by
one, which would require many additional computations and checks for duplicates.

I have tried to avoid using split as much as possible and only at the end joining a space to the result of splitting the string,
which seems to be the quickest way to remove whitespace.

In cut_utterance I have two list comprehensions, as the first is meant to be for groups starting at the beginning of the string
so that not all iteration have to recheck, if the group is starting at the beginning.  The second group starts at
the second character.

Some of the tests have taken free text files from the internet, therefore they require internet access.  As the online files 
may change, these tests may become obsolete.
