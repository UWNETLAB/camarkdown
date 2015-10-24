Class for full WOS records

It [is meant to be immutable; many of the methods and attributes](^tag1) are [evaluated when first called, not when the object is created,]($tag2) and the results are stored in a private dictionary.

The record's meta-data is stored in an ordered dictionary labeled by WOS tags. To access the raw data stored in the original record the [getTag()]({{ site.baseurl }}{% post_url /docs/2015-09-30-Record %}#Record) method can be used. To access data that has been processed and cleaned the attributes named after the tags are used.

##### Customizations

The Record's hashing and equality testing are based on the WOS number (the tag is 'UT', and also called the accession numb[er). They are strings starting with "WOS:" and followed by 15 or so numbers and letters, although both the length and character set are known to vary. The numbers are unique to each record so are used for comparisons. If a record is `bad`  al](@tag1)l equality checks return `False`.[

When converted to a string the records ti](^tag3)tle is used so for a record `R`, R.TI == R.title == str(R).

##### Attributes

When a [record is created if the parsing of](^tag1 ^tag2) the WOS file failed it is marked as `bad`. The `bad` attribute is set to True and the `error` attribute is created to contain the exception object.

Generally, to get the information from a Record its attributes should be used. For a Record `R`, calling `R.CR` causes [citations()]({{ site.baseurl }}{% post_url /docs/2015-09-30-tagFuncs %}#tagFuncs) from the the [tagFuncs]({{ site.baseurl }}{% post_url /docs/2015-09-30-tagFuncs %}#tagFuncs) module to be called on the contents of the raw 'CR' field. Then the result is saved and returned. In this case, a list of Citation objects is returned. You can also call `R.citations` to get the same effect, as each known field tag has a longer name (currently there are 61 field tags). These names are meant to make accessing tags more readable and mapping from tag to name can be found in the tagToFull dict. If a tag is known [[(in [tagToFull]({{ site.baseurl }}{% post_url /docs/2015-09-30-metaknowledge %}#metaknowledge)) but](^tag1) not](^tag2) in the raw data `None` is returned instead. Most tags when cleaned return a string or list of strings, the exact results can be found in the help for the particular function.

The attribute `authors` is also defined as a convience and returns the same as 'AF' or if that is not [found](^tag4) 'AU'.
