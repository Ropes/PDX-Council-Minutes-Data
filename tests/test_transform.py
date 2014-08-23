from __future__ import unicode_literals, print_function
import re
import datetime
import codecs
from pprint import pformat
import os
from sys import stderr
import unittest

from ops.transform import (stop, stop_set, stop_words, freq_dist_count, stem_text,\
                freq_dist_dict, remove_punctuation, token_index, \
                stop_word_placeheld, split_minutes_content,\
                split_statements_from_discussion, split_statements_via_colon)

base_resources = '{}/tests/resources/'.format(os.getcwd())
target_out = '{}/tests/target/'.format(os.getcwd())


class TestTransformOps(unittest.TestCase):
    ick_str = 'adams: wat, badcat. x:cat. $9,000'
    good_str = 'adams wat badcat xcat $9000'
    punct = ',:.?!"\''
    small_text = "The quick brown fox jumps over the lazy dog which looks like a fox so we can quick jump to get repeated words."
    small_unicode = u""

    def test_stop_words(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            #print(text, file=stderr)
            stopped = stop_words(text)  
            #print(stopped, file=stderr)
            self.assertGreater(len(stopped.split()), 50)
            self.assertNotEqual(text, stopped)

    def test_stop_words_decode_fail(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read()
            self.assertRaises(UnicodeDecodeError, stop_words, text)

    def test_stop_word_placeheld(self):
        stopped = stop_word_placeheld(self.small_text)
        print(pformat(stopped))
        self.assertEqual(stopped[0], '')
        self.assertEqual(stopped[1], 'quick')
        self.assertEqual(stopped[6], '')


    def test_freq_dist(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            #print(text, file=stderr)
            stopped = stop_words(text)  

            freq_dist = freq_dist_count(stopped.split()) 
            #print(pformat(freq_dist), file=stderr)
            self.assertGreater(len(freq_dist), 50)

    def test_stemming(self):
        with open('{}{}'.format(base_resources, 'lebowskiIpsum'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            #print(text, file=stderr)
            stemmed = stem_text(text)
            #print('Stemmed:\n'+stemmed, file=stderr)
            self.assertGreater(len(stemmed.split()), 50)
            
    
    def test_stop_words_full(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  
            with open('{}{}'.format(target_out, '2011-1-19stopped'), 'w')\
            as out_file:
                out = ''.join(stopped)
                out_file.write(out.encode('utf8'))
        

    def test_freq_dist_full(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            assert type(text) == unicode
            stopped = stop_words(text)  
            freq_dist = freq_dist_count(stopped.split()) 
            #print(pformat(freq_dist), file=stderr)
            with open('{}{}'.format(target_out, '2011-1-19freq_dist_count'), 'w')\
            as out_file:
                out_file.write(pformat(freq_dist))


    def test_freq_dist_dict_full(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            stopped = stop_words(text)  
            freq_dist = freq_dist_dict(stopped.split()) 
            #print(pformat(freq_dist), file=stderr)
            self.assertGreater(freq_dist[u'year'], 8)
            self.assertLess(freq_dist[u'year'], 12)

            text = remove_punctuation(text)
            stopped = stop_words(text)  
            freq_dist = freq_dist_dict(stopped.split())
            #print(pformat(freq_dist), file=stderr)
            self.assertGreater(freq_dist[u'year'], 16)

            with open('{}{}'.format(target_out, '2011-1-19freq_dist_dict'),\
            
            'w') as out_file:
                out_file.write(pformat(freq_dist))

    def test_punctuation_removal_str(self):
        x = str(self.ick_str)
        out = remove_punctuation(x, punct=self.punct)
        self.assertEqual(out, self.good_str)
        #print(type(out), file=stderr)

    def test_punctuation_removal_unicode(self):
        x = unicode(self.ick_str)  
        out = remove_punctuation(x, punct=self.punct)
        self.assertEqual(out, unicode(self.good_str))
        #print(type(out), file=stderr)

    def test_token_index_simple(self):
        tk_str = 'adams wat badcat xcat $9000 xcat'
        ti = token_index(tk_str)
        print(ti)
        self.assertIn(1, ti['wat'])
        self.assertIn(3, ti['xcat'])
        self.assertIn(5, ti['xcat'])

    def test_freq_dist_dict_full(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            text = remove_punctuation(text)
            stopped = stop_words(text)  
            ti = token_index(stopped)
            #print(pformat(ti), file=stderr)
            with open('{}{}'.format(target_out, '2011-1-19token_index'),\
            
            'w') as out_file:
                out_file.write(pformat(ti))

    def test_stop_list(self):
        self.assertEqual(type(stop), list)
        self.assertEqual(type(stop_set), set)

        word = list(stop_set)[0]
        self.assertEqual(type(word), unicode)

    def test_split_content(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), 'r')\
        as f:
            text = f.read().decode('utf-8')
            text = ''.join(text)
            split_doc = split_minutes_content(text)
            self.assertEqual(len(split_doc), 2)
            #print(split_doc[0], file=stderr)

    def test_split_discussion(self):
        with open('{}{}'.format(base_resources, '2011-1-19raw.txt'), mode='r')\
        as f:
            text = f.read().decode('utf8')
            text = ''.join(text)

            split_doc = split_minutes_content(text)
            self.assertEqual(len(split_doc), 2)

            print(split_doc[1][:3000])
            #convos = split_statements_from_discussion(split_doc[1])
            trans_table = dict.fromkeys(map(ord, u"\n"), None)
            print(trans_table)
            sp_text = split_doc[1].translate(trans_table)
            print(sp_text)
            convos = split_statements_via_colon(sp_text)

            #print("Statements found: {}".format(convos[:5]))
            for i in range(0, 50):
                print(unicode(convos[i]))
            self.assertGreater(len(convos), 100)
            self.assertEqual(1, 2)

    def test_split_text(self):
        text = '''operating much more efficiently.    Fritz: So the projection is for --   Adams: If I can add on to that.  The greater sales effort to businesses, to sign up for validation, means more uses of the garage, so aggressive sales pitch to businesses has the opportunity in increasing the -- increasing the validation program has the opportunity to bring in more revenue.    Fritz: And --   Geason:  And the cost in the garage will be done with the use of technology.    Fritz: We're not projecting to increase the parking fees?   Geason:  Not at this time.    Fritz: The projection is for $11 million a year in revenue.  How much do we currently get?   Geason: $10 million.    Fritz: About an million increase.  Thank you.  We have had a discussion when reviewing the handy capped permits, but the possibility of allowing the use of handy capped spaces to be used without '''

        convos = split_statements_from_discussion(text)

        #print("Statements found: {}".format(convos[:5]))
        speakers = set()
        print('\n\n')
        for c in convos:
            speakers.add(c[0].strip())
            print('{}->"{}"'.format(c[0].strip(), c[1].strip()))
        #self.assertEqual(len(convos), 100)
        self.assertTrue("Fritz" in speakers)
        self.assertTrue("Adams" in speakers)

    def test_split_text_with_brackets(self):
        text = '''
meeting and the public is welcomed to weigh in on these throughout the budget process.    Fish: Aye.  Leonard: Aye.  Saltzman: Aye.    Adams: Aye 60 is approved.  [gavel pounded] please read the title for emergency ordinance number 61. Item 61.    Adams: Commissioner Fritz. Fritz: thank you, mayor.  I'm pleased to bring before council an audit settlement with mci metro negotiated by our office of cable communication and franchise management in cooperation with the city attorney's office, it was based on a well-done audit pursuant to an ongoing successfu '''
        convos = split_statements_from_discussion(text)
        speakers = set()
        for c in convos:
            speakers.add(c[0].strip())
            #print('{}->"{}"'.format(c[0].strip(), c[1].strip()))
        
        self.assertTrue("Saltzman" in speakers)
        self.assertTrue("Fritz" in speakers)
        self.assertTrue("Adams" in speakers)

    def test_split_text_by_colon(self):
        text = '''
meeting and the public is welcomed to weigh in on these throughout the budget process.    Fish: Aye.  Leonard: Aye.  Saltzman: Aye.    Adams: Aye 60 is approved.  [gavel pounded] please read the title for emergency ordinance number 61. Item 61.    Adams: Commissioner Fritz. Fritz: thank you, mayor.  I'm pleased to bring before council an audit settlement with mci metro negotiated by our office of cable communication and franchise management in cooperation with the city attorney's office, it was based on a well-done audit pursuant to an ongoing successfu   '''
        text += '''operating much more efficiently.    Fritz: So the projection is for --   Adams: If I can add on to that.  The greater sales effort to businesses, to sign up for validation, means more uses of the garage, so aggressive sales pitch to businesses has the opportunity in increasing the -- increasing the validation program has the opportunity to bring in more revenue.    Fritz: And --   Geason:  And the cost in the garage will be done with the use of technology.    Fritz: We're not projecting to increase the parking fees?   Geason:  Not at this time.    Fritz: The projection is for $11 million a year in revenue.  How much do we currently get?   Geason: $10 million.    Fritz: About an million increase.  Thank you.  We have had a discussion when reviewing the handy capped permits, but the possibility of allowing the use of handy capped spaces to be used without '''

        convos = split_statements_via_colon(text)

        speakers = set()
        for c in convos:
            speakers.add(c.speaker)
            print(c)
        
        self.assertTrue("Saltzman" in speakers)
        self.assertTrue("Fritz" in speakers)
        self.assertTrue("Adams" in speakers)

        self.assertEqual(1,2)
