The Record's hashing and equality testing are based on the WOS number (the tag is 'UT', and also called the accession number). They are strings starting with "WOS:" and followed by 15 or so numbers and letters, although both the length and character set are known to vary. The numbers are unique to each record so are used for comparisons. If a record is `bad`  all equality checks return `False`.

When converted to a string the records title is used so for a record `R`, R.TI == R.title == str(R).
