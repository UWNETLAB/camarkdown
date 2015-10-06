---
layout: page
title: Record
categories: docs
excerpt: The Record Class
tags: [class]
weight: 2
---
<a name="Record"></a>
<a name="Record"></a>**Record**(_inRecord, taglist=(), sFile='', sLine=0_):

Class for full WOS records

It is meant to be immutable; many of the methods and attributes are evaluated when first called, not when the object is created, and the results are stored in a private dictionary.

The record's meta-data is stored in an ordered dictionary labeled by WOS tags. To access the raw data stored in the original record the [getTag()]({{ site.baseurl }}{% post_url /docs/2015-09-30-Record %}#Record) method can be used. To access data that has been processed and cleaned the attributes named after the tags are used.

##### Customizations

The Record's hashing and equality testing are based on the WOS number (the tag is 'UT', and also called the accession number). They are strings starting with "WOS:" and followed by 15 or so numbers and letters, although both the length and character set are known to vary. The numbers are unique to each record so are used for comparisons. If a record is `bad`  all equality checks return `False`.

When converted to a string the records title is used so for a record `R`, R.TI == R.title == str(R).

##### Attributes

When a record is created if the parsing of the WOS file failed it is marked as `bad`. The `bad` attribute is set to True and the `error` attribute is created to contain the exception object.

Generally, to get the information from a Record its attributes should be used. For a Record `R`, calling `R.CR` causes [citations()]({{ site.baseurl }}{% post_url /docs/2015-09-30-tagFuncs %}#tagFuncs) from the the [tagFuncs]({{ site.baseurl }}{% post_url /docs/2015-09-30-tagFuncs %}#tagFuncs) module to be called on the contents of the raw 'CR' field. Then the result is saved and returned. In this case, a list of Citation objects is returned. You can also call `R.citations` to get the same effect, as each known field tag has a longer name (currently there are 61 field tags). These names are meant to make accessing tags more readable and mapping from tag to name can be found in the tagToFull dict. If a tag is known (in [tagToFull]({{ site.baseurl }}{% post_url /docs/2015-09-30-metaknowledge %}#metaknowledge) but not in the raw data `None` is returned instead. Most tags when cleaned return a string or list of strings, the exact results can be found in the help for the particular function.

The attribute `authors` is also defined as a convience and returns the same as 'AF' or if that is not found 'AU'.

##### \_\_Init\_\_

Records are generally create as collections in  [Recordcollections]({{ site.baseurl }}{% post_url /docs/2015-09-30-RecordCollection %}#RecordCollection), and not as individual objects. If you wish to create one on its own it is possible, the arguments are as follows.

##### Parameters

_inRecord_: `files stream, dict, str or itertools.chain`

 If it is a file stream the file must be open at the location of the first tag in the record, usually 'PT', and the file will be read until 'ER' is found, which indicates the end of the record in the file.

 If a dict is passed the dictionary is used as the database of fields and tags, so each key is considered a WOS tag and each value a list of the lines of the original associated with the tag. This is the same form of dict that [recordParser]({{ site.baseurl }}{% post_url /docs/2015-09-30-metaknowledge %}#metaknowledge) returns.

 For a str the input is the raw textual data of a single record in the WOS style, like the file stream it must start at the first tag and end in 'ER'.

 itertools.chain is treated identically to a file stream and is used by [RecordCollections]({{ site.baseurl }}{% post_url /docs/2015-09-30-RecordCollection %}#RecordCollection).

_sFile_ : `optional [str]`

 Is the name of the file the raw data was in, by default it is blank. It is mostly used to make error messages more informative.

_sLine_ : `optional [int]`

 Is the line the record starts on in the raw data file. It is mostly used to make error messages more informative.


<a name="Record.activeTags"></a>Record.**activeTags**():

Returns a list of all the tags the original WOS record had. These are all the tags that ['getTag()']({{ site.baseurl }}{% post_url /docs/2015-09-30-Record %}#Record) will not return `None` for.

##### Returns

`List[str]`

 a list of WOS tags in the Record


<a name="Record.createCitation"></a>Record.**createCitation**():

Creates a citation string, using the same format as other WOS citations, for the [Record]({{ site.baseurl }}{% post_url /docs/2015-09-30-Record %}#Record) by reading the relevant tags (year, J9, volume, beginningPage, DOI) and using it to start a [Citation]({{ site.baseurl }}{% post_url /docs/2015-09-30-Citation %}#Citation) object.

##### Returns

`Citation`

 A [Citation]({{ site.baseurl }}{% post_url /docs/2015-09-30-Citation %}#Citation) object containing a citation for the Record.


<a name="Record.getTag"></a>Record.**getTag**(_tag, clean=False_):

Returns a list containing the raw data of the record associated with _tag_. Each line of the record is one string in the list.

##### Parameters

_tag_ : `str`

 _tag_ can be a two character string corresponding to a WOS tag e.g. 'J9', the matching is case insensitive so 'j9' is the same as 'J9'. Or it can be one of the full names for a tag with the mappings in [fullToTag](#metaknowledge). If the string is not found in the original record or after being translated through [fullToTag](#metaknowledge), `None` is returned.

##### Returns

`List [str]`

 Each string in the list is a line from the record associated with _tag_ or None if not found.


<a name="Record.getTagsDict"></a>Record.**getTagsDict**(_taglst, cleaned=False_):

returns a dict of the results of getTag, with the elements of _taglst_ as the keys and the results as the values.

##### Parameters
_taglst_ : `List[str]`

 Each string in _taglst_ can be a two character string corresponding to a WOS tag e.g. 'J9', the matching is case insensitive so 'j9' is the same as 'J9'. Or it can be one of the full names for a tag with the mappings in [fullToTag]({{ site.baseurl }}{% post_url /docs/2015-09-30-metaknowledge %}#metaknowledge). If the string is not found in the oriagnal record before or after being translated through [fullToTag](#metaknowledge), `None` is used instead. Same as in [`getTag()`]({{ site.baseurl }}{% post_url /docs/2015-09-30-Record %}#Record)

##### Returns

`dict[str : List [str]]`

 a dictionary with keys as the original tags in _taglst_ and the values as the results


<a name="Record.getTagsList"></a>Record.**getTagsList**(_taglst, cleaned=False_):

Returns a list of the results of [`getTag()`]({{ site.baseurl }}{% post_url /docs/2015-09-30-Record %}#Record) for each tag in _taglist_, the return has the same order as the original.

##### Parameters
_taglst_ : `List[str]`

 Each string in _taglst_ can be a two character string corresponding to a WOS tag e.g. 'J9', the matching is case insensitive so 'j9' is the same as 'J9'. Or it can be one of the full names for a tag with the mappings in [fullToTag]({{ site.baseurl }}{% post_url /docs/2015-09-30-metaknowledge %}#metaknowledge). If the string is not found in the original record before or after being translated through [fullToTag]({{ site.baseurl }}{% post_url /docs/2015-09-30-metaknowledge %}#metaknowledge), `None` is used instead. Same as in [`getTag()`]({{ site.baseurl }}{% post_url /docs/2015-09-30-Record %}#Record)

 Then they are compiled into a list in the same order as _taglst_

##### Returns

`List[str]`

 a list of the values for each tag in _taglst_, in the same order


<a name="Record.writeRecord"></a>Record.**writeRecord**(_infile_):

Writes to _infile_ the original contents of the Record. This is intended for use by [RecordCollections]({{ site.baseurl }}{% post_url /docs/2015-09-30-RecordCollection %}#RecordCollection) to write to file. What is written to _infile_ is bit for bit identical to the original record file. No newline is inserted above the write but the last character is a newline.

##### Parameters

_infile_ : `file stream`

 An open utf-8 encoded file



{% include docsFooter.md %}
