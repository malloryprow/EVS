#!/usr/bin/env python3
'''
Name: send_mail_write_messages.py
Contact(s): Mallory Row (mallory.row@noaa.gov)
Abstract: This writes the message files to be sent
          to alert for missing data.
Run By: scripts/mail/send/exevs_send_mail.sh
'''

import os
import datetime
import sys
import glob
import numpy as np
import pandas as pd

print("BEGIN: "+os.path.basename(__file__))

# Read in environment variables
DATA = os.environ['DATA']
NET = os.environ['NET']
RUN = os.environ['RUN']
COMIN = os.environ['COMIN']
COMOUT = os.environ['COMOUT']
SENDCOM = os.environ['SENDCOM']
STEP = os.environ['STEP']
COMPONENT = os.environ['COMPONENT']
VDATE = os.environ['VDATE']
vhr = os.environ['vhr']

# Get sendmail files
sendmail_file_list = (
    glob.glob(os.path.join(COMIN, 'prep', '*', '*', 'sendmail', '*'))
    +
    glob.glob(os.path.join(COMIN, 'stats', '*', '*', '*', '*', 'sendmail', '*'))
)

# Read sendmail files
for sendmail_file in sendmail_file_list:
    sendmail_file_df = pd.read_csv(
        sendmail_file, sep=':',header=None, dtype=str,
        skipinitialspace=True
    ).T
    sendmail_file_df.columns = sendmail_file_df.iloc[0]
    sendmail_file_df = sendmail_file_df.drop(sendmail_file_df.index[0])

print("END: "+os.path.basename(__file__))
