A quick and dirty mailer class that I made for a batch mail.
Built on conda base Python 3.7, probably works with just standard libraries,
in Python 3.6+. (f-strings are great)

student_mail_example is an example and my use case for this: a script that takes a .tsv with names and e-mails and a folder with the same number of pdfs, sorted, and sends the j-4 to the j-1th pdf to the jth person.

Copy-pasted most of the code that does the real work from: https://realpython.com/python-send-email/
Also check that article for how to set up a Gmail account you can use for automated mails.

I added a flexible batch_mail function that can take single or iterable values for most of its arguments.

Warning: some snippets of the class are untested, thus probably broken.
