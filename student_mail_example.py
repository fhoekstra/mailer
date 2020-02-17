from pathlib import Path

import numpy as np

from send_mail import setup_mailer
from utility import indexchoice
import pers_info  # Personal info I don't want to check in to Github
# ^This is just the e-mail address I send the mails from

################# PARAMETERS #################
filespath = Path(__file__).resolve().parent / 'Assessment 2 - 2020'

# Now get list of receivers from Google Form csv file
tsvlist = []
for pth in filespath.glob('*.tsv'):
    tsvlist.append(pth)
if len(tsvlist) == 1:
    tsv = tsvlist[0]
else:
    tsv = tsvlist[indexchoice(tsvlist)]
tsvarr = np.genfromtxt(tsv, dtype=None, delimiter='\t', encoding=None)
studmails = tsvarr[1:, 1]  # This is it!
studnames = tsvarr[1:, 2]

# And get docs from folder.
pdflist = sorted(filespath.glob('[0-9][0-9].pdf'))
#print(studmails, len(pdflist))
assert len(pdflist) == len(studmails)
N = len(pdflist)

########## CHECK CHECK DOUBLE-CHECK ##############
# Make a mapping from studidx to pdfidx
maildocmap = {}  # {receiveridx: (pdfidx0, pdfidx1, ... pdfidx3)}
for j in range(len(studmails)):  # j is index
    if j == 0:
        maildocmap[j] = tuple(range(N - 4, N))
    elif j < 4:
        # import pdb; pdb.set_trace()
        maildocmap[j] = tuple(
            list(range( N - (4 - j), N))
            + list(range(j)))
    else:
        maildocmap[j] = tuple(range(j-4, j))
print(maildocmap)
# Compile the attachments paths list
attachments = []
for studidx in range(N):
    thesefiles = [pdflist[pdfidx] for pdfidx in maildocmap[studidx]]
    attachments.append(thesefiles)
    print(f'{studidx}  : {[fl.name for fl in thesefiles]} , {studmails[studidx]}')

# Write the body
subject = "Editor's Decision Assessment 2"
messages = []
for name in studnames:
    messages.append(f"Dear editors in the group of {name},\n"
    + f"Please use the included reviewer's reports to make a decision about the paper.\n"
    + f"Use the form at {pers_info.form_link} \n"
    + """Your decision (and message to the authors) is required by Thursday next week.
    
    Regards,
    The Organisers"""
    + f"P.S. This message was automatically generated. If one of the attachments is your own report, please send an e-mail to {pers_info.private_mail}"
    )


########## ONE BATCH TO RULE THEM ALL #############

mailer = setup_mailer(username=pers_info.my_mail_full)
mailer.batch_mail(pers_info.my_mail_full, studmails, subject, messages,
                   attachments=attachments, attachdifpermail=True)
