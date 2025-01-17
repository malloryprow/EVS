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
import pandas as pd
import time
import shutil
import subprocess

print("BEGIN: "+os.path.basename(__file__))

# Read in environment variables
DATA = os.environ['DATA']
NET = os.environ['NET']
RUN = os.environ['RUN']
COMIN = os.environ['COMIN']
COMOUT = os.environ['COMOUT']
SENDCOM = os.environ['SENDCOM']
SENDMAIL = os.environ['SENDMAIL']
MAILTO = os.environ['MAILTO']
MAILCC = os.environ['MAILCC']
STEP = os.environ['STEP']
COMPONENT = os.environ['COMPONENT']
VDATE = os.environ['VDATE']
vhr = os.environ['vhr']
USER = os.environ['USER']

# Set up date information
VDATEvhr_dt = datetime.datetime.strptime(VDATE+vhr, '%Y%m%d%H')
VDATEvhr_m6hr_dt = VDATEvhr_dt - datetime.timedelta(hours=6)
print("Using missing data files created between "
      f"{VDATEvhr_m6hr_dt:%Y%m%d %HZ} and {VDATEvhr_dt:%Y%m%d %HZ}")

# sendmail columns
sendmail_col_list = [
    'Data Source', 'File Path', 'Valid Time',
    'Initialization Time', 'Forecast Hour', 'Status'
]

# Get sendmail files
prep_sendmail_path = os.path.join(COMIN, 'prep', '*', '*', 'sendmail', '*')
stats_sendmail_path = os.path.join(COMIN, 'stats', '*', '*', '*', '*',
                                   'sendmail', '*')
print(f"Looking at missing data files in {prep_sendmail_path} "
      +f"and {stats_sendmail_path}")
sendmail_file_list = (
    glob.glob(prep_sendmail_path) + glob.glob(stats_sendmail_path)
)

# Read sendmail files
sendmail_df_list = []
for sendmail_file in sendmail_file_list:
    sendmail_file_ctime_dt = datetime.datetime.strptime(
        time.ctime(os.path.getctime(sendmail_file)),
        '%a %b %d %H:%M:%S %Y'
    )
    if sendmail_file_ctime_dt < VDATEvhr_m6hr_dt \
            or sendmail_file_ctime_dt > VDATEvhr_dt:
        continue
    sendmail_file_df = pd.read_csv(
        sendmail_file, sep=':',header=None, dtype=str,
        skipinitialspace=True
    ).T
    sendmail_file_df.columns = sendmail_file_df.iloc[0]
    sendmail_file_df = sendmail_file_df.drop(sendmail_file_df.index[0])
    sendmail_file_df_list = []
    for sendmail_col in sendmail_col_list:
        if sendmail_col in sendmail_file_df.columns.tolist():
            sendmail_file_df_list.append(
                sendmail_file_df[sendmail_col].values[0]
            )
        else:
            sendmail_file_df_list.append('NA')
    sendmail_df_list.append(sendmail_file_df_list)
sendmail_df = pd.DataFrame(sendmail_df_list, columns=sendmail_col_list)
sendmail_df['Data Source'] = sendmail_df['Data Source'].str.upper()

# Consolidate by Data Source
sendmail_df_groupby = sendmail_df.groupby(['Data Source'])
for group in sendmail_df_groupby.groups.keys():
    # Filter through data source's missing file(s)
    print(f"Reviewing missing data files for data source {group}")
    sendmail_df_groupby_group = sendmail_df_groupby.get_group(group)
    group_file_path_list = (
        sendmail_df_groupby_group['File Path'].values.tolist()
    )
    tmp_sendmail_group_file = os.path.join(DATA, f"{group}_{VDATE}{vhr}.txt")
    with open(tmp_sendmail_group_file, 'w') as tsgf:
        tsgf.write("The following files are missing for data source "
                   +f"{group}:\n")
        for group_file_path in group_file_path_list:
            tsgf.write(f"{group_file_path}\n")
    # Send file to COMOUT
    if SENDCOM == 'YES':
        output_sendmail_group_file = os.path.join(
            COMOUT+f".{VDATE}", tmp_sendmail_group_file.rpartition('/')[2]
        )
        print(f"Copying {tmp_sendmail_group_file} to "
              +output_sendmail_group_file)
        shutil.copy(tmp_sendmail_group_file, output_sendmail_group_file)
    # Send email
    #### If USER starts with ops. - send using prod_util's mail.py
    #### Otherwise use mail
    if SENDMAIL == 'YES':
        subject=f"EVS: Missing Data from data source {group}"
        mail_recipients = MAILTO
        if len(MAILCC) != 0:
             mail_recipients =  f"{mail_recipients},{MAILCC}"
        if USER in ['ops.prod', 'ops.para']:
            mail_cmd = ['mail.py', '-s', '"'+subject+'"',
                        '-c', '"'+mail_recipients+'"',
                        '<', tmp_sendmail_group_file]
        else:
            mail_cmd = ['cat', tmp_sendmail_group_file, '|', 'mail',
                        '-s', '"'+subject+'"', '"'+mail_recipients+'"']
        print(f"Running {' '.join(mail_cmd)}")
        sp_mail_cmd = subprocess.run(' '.join(mail_cmd), shell=True)
        if sp_mail_cmd.returncode != 0:
            print(f"ERROR: {' '.join(sp_mail_cmd.args)} gave return code "
                  +f"{str(sp_mail_cmd.returncode)}")
            sys.exit(sp_mail_cmd.returncode)

print("END: "+os.path.basename(__file__))
