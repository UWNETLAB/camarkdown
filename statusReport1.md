# caMarkdown Status report 1

## Overview

As caMarkdown stands now there are 7 subCommands:
    - init
    - status
    - add
    - tag
    - table
    - sync
    - organize

The first 3 are loosely based on the git commands of the same names. The tag command is used to get information about tags. table outputs a table of counts. While sync and organize handle the codebook, sync adds to it organize sorts it.

The actual structure of files expected by the program is similar to git. The files are all within one directory or its subdirectories and there are a few special files/directories at the top that control things.

The most important file is the codebook. The codebook contains all the information about the codes as well as all the files. Right now it is quite basic, There are blank lines, comment lines, file path lines and code lines. Code lines start with a code character ('@', '^', or '$') then can have a semicolon and a description. Comments are indicated with '#' which causes the rest of the line to be ignored. While file path lines are everything else.

The systems are quite sparse right now and need more testing then some use. To find bugs and determine how to make them most usable by humans.


## Behind the scenes

I have structured the caMarkdown program as a python module, i.e. something you can install with pip and import. The file handling/manginging the directory tree is done by one class `Project`. This is what all of the subCommands are using. They then call different methods of the object. I did it this way so that error handling and much of the boilerplate could be put in one place instead of inside each subCommand.

The parsing of actual files is done by a second object called `parseTree`. These hold the parsing trees of whole files and can be be combined to make one projects tree. The trees then produce `Tag` objects, actually subclasses each code type has its own one.

`Tag` objects handle the codes in the code book. There are 2 parts to a tag the first character indicating its type and the rest giving its name, e.g. `"^tag1"` has type meta and the name `"tag1"`. Tags then have any number of `CodeSection` objects which are the actual substrings of the documents the tags are annotating. They also contain information about the file and the other `CodeSections` inside it.

Basically the two important classes `Project` and `Tag`, the former for file handling the latter for parsing and getting information at a granular level.

## Where things are now

I think more than half of the commands in the original design plan have been implemented as well as a few other. I actually wrote `tag` because I though it was an obvious feature and then noticed it was `extract` from the original docs.

The next big thing to do is either flush out the features or add git.

There are also a good number of smaller things that need to be sorted out and I would like your feedback on.

## Questions

1. Vocabulary:
    - I have been using the words tag and code interchangeably, I feel code is the thing that has meaning while tag is simply a simple string to label the code but I could be wrong.
    - What is the name of the directory tree caMarkdown works on? I used project but I also feel repo would be valid.

2. Name:
    - John Gruber is know for being protective of the name Markdown. I do not think he will discover this but it might still be good to consider not using the work "Markdown" anywhere. "caMark" is the obvious step away from Markdown. What are your thoughs?

3. YAML:
    - Dealing with the codebook so far has been fine. But that is because I severely limited what could be in it. I think making the whole book YAML might make things easier for me and much less likely to break if a new feature is added.

4. Your thoughts:
    - What are they?
    - Should I have done this as a couple slack posts?
