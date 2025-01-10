#!/bin/bash
###############################################################################
# Name of Script: exevs_send_mail.sh
# Developers: Mallory Row / Mallory.Row@noaa.gov
# Purpose of Script: This script is runs for the send mail step
###############################################################################

set -x

echo

# Run script to go through evs sendmail directories and write messages for emails
python ${USHevs}/send/send_mail_write_messages.py
export err=$?; err_chk
