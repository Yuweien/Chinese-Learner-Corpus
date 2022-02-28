#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:16:41 2019

@author: yuwei
"""

# A Basic Searching Program for a Chinese Learners' Corpus
#============
"""This script provide a basic searching window for a Chinese Learners' Corpus, 
in which people can search words or regex in the corpus, 
display the searched words in its context, 
count the frequency of the words in corpus, and save the searched results into files.
The data for this program is packed in 'Chinese corpus' folder."""

#Example usage
# -------------
# ./corpusTool.py myDirectory/*.txt

# Now try to search something!
# searching suggestions:
# functional words: 了， 是， 的
# Chinese classifiers:一.|二.|两.|三.|四.|五.|六.|七.|八.|九.|十.|这.|那.|哪.
# verbs with temporal aspects: .了|.过|在.|正在.

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import re,os
import sys

if __name__ == "__main__":
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    #Parse the command line input
    parser = ArgumentParser(
        description="corpusTool.py",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    #Take the file names as argument for the next function
    parser.add_argument(
        "input", type=str, nargs="+", help="Input .txt files"
    )
    args = parser.parse_args()

    #Read in all the files, and store the body of the text into a string
    corpus = ''
    for file in args.input:
        f = open(file,'r')
        t = f.read()
        t = re.sub('\w+\d{4}_\d{3}_\d+\w+\n','',t) #remove header


        corpus += t  
        f.close()

    
    #Function to list the searching result
    def Egetresult():
        st.delete(1.0,'end') #delete what's in the scrolled text, clear the window for each research
        pat = e.get() #get the entered string as regex pattern
        words = re.findall(pat,corpus) #search in corpus
        res = '' #start a empty string to store the result
        if words: # if matched the pattern 
            pat2 = '(.{25})('+ pat + ')(.{25})' #give back the pattern and its context
                                            #(25 characters before and after)
                                            #put the pattern into parenthesis for the upcoming highlighting
            t = re.findall(pat2,corpus)
            for i in t: #to check if there are other matched patterens in the context
                t2 = re.findall(pat,i[0]+i[2])
                if t2: #if there are other matched patterns, find all of them in the matched line
                    #(including the original matched one)
                    x = i[0]+i[1]+i[2]
                    t3 = re.findall(pat,x)
                    for n in range(len(t3)): #replace each matched words with the words surrounded in angle brackets
                        if t3[n] not in t3[n+1:]: #but if there are identical matched members in t3, 
                                                #do not substitute multipel times
                            x = re.sub(t3[n],'<'+t3[n] +'>',x)
                    res += x + '\n' #increment the highlighted matched context
                else:
                    res += i[0]+'<'+i[1] +'>'+i[2]+'\n' #normal case, highlight the matched pattern
            
            #Caculate the token and frequency, and concatenate all the stuff together
            res = res + 'word token: '+ str(len(words))+'\t'+'word frequency:'+str(len(words)/len(corpus))
            st.insert(INSERT,res)#fill the result into the scrolltext
            return res
        else:
        #if the pattern is not matched at all in the corpus, say sorry.
            res = 'Sorry, I find nothing related in this corpus.'
            st.insert(INSERT,res)
        
    def Save(): #Write the results into files
        fname = 'searching_'+e.get()+'.txt' #create txt files with names of the searched words"
        f = open(fname,'w')
        x = Egetresult() #write the searching result
        f.write(x)
        f.close()
    
    r = Tk() #start up GUI system
    r.title("Arizona Chinese Learners' Corpus") #rename the title of the window
    f = Frame(r,width=1400,height=700) #make a window
    f.pack() #display that window

    b1 = Button(  #make a Quit button
        r,
        text = 'Quit',
        command = r.destroy,
    )

    b2 = Button(  #make a Look up button
        f,
        text='Look up',
        command = Egetresult,
    )

    b3 = Button(  #make a Save button
        f,
        text = 'Save the result',
        command = Save,
    )

    st = ScrolledText(  #make a scrolledtext
        r,
        bg = "#fffad6",  # give a backgroud color, I like bright yellow
        width = 105,height = 45
    )

    l = Label(  #make a Lable to welcome users
        f,
        text = "Welcome to Arizona Chinese Learners' Corpus",
        font = "none 16 bold",
    )

    e = Entry( #make a Entry box
        f,
    )

    l.pack()
    e.pack()



    e.insert(0,'是')
    #e.insert(0,'Start searching here')
    st.pack(anchor=CENTER)
    st.insert(INSERT,"(The result is going to show here)")
    b2.pack()
    b3.pack()
    b1.pack()

    mainloop()



