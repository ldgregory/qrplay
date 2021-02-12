#! /usr/bin/env python3

"""
Leif Gregory <leif@devtek.org>
qrplay.py v0.1
Tested to Python v3.8.5

Description:
Generate QR codes for various actions:
- Bitcoin Address
- Calendar / iCal
- Email
- Facetime
- Map lat/long coords in decimal degrees e.g. (-)xxx.xxxxx, (-)xxx.xxxxx
- Call a number
- Save the QR image to PNG file
- Make a Skype video call
- Send an SMS
- URL
- vCard
- Connect to a WiFi SSID
- Open a Youtube video

These have all been tested with iOS 14.4

Dependencies:
pip install qrcode[pil]

Changelog:
20200211 -  Added bitcoin, calendar, redo of argparse options.
20191127 -  Initial code

Copyright 2020 Leif Gregory

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import argparse
import qrcode
from datetime import datetime
from datetime import timezone


class TextColor:
    BLOGR = str('\033[7;32m')
    BLUE = str('\033[1;34m')
    GREEN = str('\033[1;32m')
    PURPLE = str('\033[1;35m')
    RED = str('\033[1;31m')
    RESET = str('\033[0m')
    YELLOW = str('\033[1;33m')


def main():
    parser = argparse.ArgumentParser(description='Generate Various QR codes')
    parser.add_argument('--type',
                        dest='type',
                        help='''Type of QR code:
                        bitcoin
                        calendar
                        email
                        facetime
                        map
                        phone
                        skype
                        sms
                        vcard
                        wifi
                        youtube''')
    parser.add_argument('--save', help='Save image as filename.png', dest='filename')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0', dest='version')
    args = parser.parse_args()

    """
    ERROR_CORRECT_L = About 7% or less errors can be corrected.
    ERROR_CORRECT_M = (default) = About 15% or less errors can be corrected.
    ERROR_CORRECT_Q = About 25% or less errors can be corrected.
    ERROR_CORRECT_H = About 30% or less errors can be corrected.
    """

    # Instantiate object with some basic configuration
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=15,
        border=4,
    )

    # Bitcoin link
    if args.type.lower() == 'bitcoin':
        account = input('Account: ')
        label = input('Label: ')
        message = input('Message: ')
        amount = input('Amount: ')
        qr.add_data(f'bitcoin:{account}?label={label}&message={message}&amount={amount}')

    # Calendar / iCal
    elif args.type.lower() == 'calendar':
        title = input('Title: ')
        location = input('Location (optional): ')
        url = input('URL (optional): ')
        description = input('Description (optional): ')
        start = input('Start Date (YYYYMMDD HHMM): ')
        end = input('End Date (YYYYMMDD HHMM): ')

        eventStart = datetime.strptime(start, "%Y%m%d %H%M").astimezone(tz=timezone.utc)
        eventEnd = datetime.strptime(end, "%Y%m%d %H%M").astimezone(tz=timezone.utc)

        qr.add_data(f'''
BEGIN:VEVENT
SUMMARY:{title}
LOCATION:{location}
URL;VALUE=URI:{url}
DESCRIPTION:{description}
DTSTART:{eventStart.strftime('%Y%m%dT%H%M00Z')}
DTEND:{eventEnd.strftime('%Y%m%dT%H%M00Z')}
END:VEVENT
''')

    # Create an email
    elif args.type.lower() == 'email':
        to = input('TO: ')
        subject = input('Subject: ')
        body = input('Body: ')
        qr.add_data(f'mailto:{to}?subject={subject}&body={body}')

    # Facetime a telephone number
    elif args.type.lower() == 'facetime':
        phone = input('Phone: ')
        qr.add_data(f'FACETIME:{phone}')

    # Geo-coords in mapping app
    elif args.type.lower() == 'map':
        lat = input('Latitude: ')
        lon = input('Longitude: ')
        qr.add_data(f'geo:{lat},{lon}')

    # Call a telephone number
    elif args.type.lower() == 'phone':
        phone = input('Phone: ')
        qr.add_data(f'TEL:{phone}')

    # Skype
    elif args.type.lower() == 'skype':
        userid = input('User ID: ')
        title = input('Title: ')
        qr.add_data(f'skype:{userid}?call&video=true;Title:{title};')

    # Create an SMS
    elif args.type.lower() == 'sms':
        phone = input('Phone: ')
        message = input('Message: ')
        qr.add_data(f'SMSTO:{phone}:{message}')

    # URL Link
    elif args.type.lower() == 'url':
        url = input('URL: ')
        qr.add_data(f'{url}')

    # Bizcard / vCard
    elif args.type.lower() == 'vcard':
        print("Hit enter to leave fields blank.\r\n")
        lastName = input('Last Name: ')
        firstName = input('First Name: ')
        jobTitle = input('Title: ')
        company = input('Company: ')
        workEmail = input('Work Email: ')
        businessAddress = input('Work Address: ')
        businessPhone = input('Work Phone: ')
        businessFax = input('Work Fax: ')
        businessUrl = input('Work URL: ')
        homeAddress = input('Home Address: ')
        homePhone = input('Home Phone: ')
        homeEmail = input('Home Email: ')

        qr.add_data(f'''
BEGIN:VCARD
VERSION:3.0
N:{lastName};{firstName}
FN:{firstName} {lastName}
TITLE:{jobTitle}
ORG:{company}
EMAIL;TYPE=WORK:{workEmail}
URL;TYPE=WORK:{businessUrl}
TEL;TYPE=WORK,VOICE:{businessPhone}
ADR;TYPE=WORK:{businessAddress}
FAX;TYPE=WORK:{businessFax}
EMAIL;TYPE=HOME:{homeEmail}
TEL;TYPE=HOME,VOICE:{homePhone}
ADR;TYPE=HOME:{homeAddress}
END:VCARD
''')

    # Connect to a wifi network
    elif args.type.lower() == 'wifi':
        ssid = input('SSID: ')
        security = input('WEP/WPA/WPA2/nopass: ')
        if security.lower() != 'nopass':
            password = input('Password: ')
        qr.add_data(f'WIFI:S:{ssid};T:{security};P:{password};;')

    # Youtube
    elif args.type.lower() == 'youtube':
        url = input('URL: ')
        qr.add_data(f'youtube://{url}')

    # Let's make an image and show it
    qr.make(fit=True)
    img = qr.make_image()
    img.show()

    # Save image if --save flag
    if args.filename:
        # If extension is not .png, strip extension and make it .png
        outFile = args.filename.split('.')[0] + '.png'
        img.save(outFile)


if __name__ == '__main__':
    main()
