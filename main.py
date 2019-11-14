#!/usr/bin/env python3
'''
https://github.com/dhruvildave
'''

import argparse
import csv
import getpass
import imghdr
import smtplib
from email.message import EmailMessage

import pyqrcode


def main(args: argparse.Namespace) -> None:
    '''Driver code'''

    sender_addr = input('Email ID: ')
    sender_pass = getpass.getpass('Password: ')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_addr, sender_pass)

        with open(args.file) as csvfile:
            names = csv.reader(csvfile)
            num = 0
            for name in names:
                details = ', '.join(name[1:])
                url = pyqrcode.create(details)
                title = name[0] + '.png'
                url.png(title, scale=8)

                msg = EmailMessage()
                msg['Subject'] = 'Invitation to Dance Party'
                msg['From'] = sender_addr
                msg['To'] = name[0]
                msg.set_content('You have been invited')

                with open(title, 'rb') as img:
                    file_data = img.read()
                    file_type = imghdr.what(img.name)
                    file_name = img.name
                    msg.add_attachment(file_data,
                                       maintype='image',
                                       subtype=file_type,
                                       filename=file_name)

                smtp.send_message(msg)
                num += 1

            print('Sent {} emails successfully!!!'.format(num))


if __name__ == '__main__':
    import sys

    parser = argparse.ArgumentParser()

    parser.add_argument('-f',
                        '--file',
                        help='Name of csv files to read input from')
    args = parser.parse_args()

    if args.file is None:
        parser.print_help()
        sys.exit(1)

    main(args)
