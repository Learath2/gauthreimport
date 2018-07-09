#!/usr/bin/env python3
import sys
import os
import pyqrcode
import sqlite3

def main():
    if len(sys.argv) is not 2:
        print('Missing argument')
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print('File {file} does not exist.'.format(file=sys.argv[1]))
        sys.exit(1)

    conn = sqlite3.connect('file:{path}?mode=ro'.format(path=sys.argv[1]), uri=True)
    c = conn.cursor()

    c.execute('SELECT * FROM accounts')
    all_rows = c.fetchall()
    conn.close()

    for acc in all_rows:
        print(acc[1])
        if acc[6] is not None:
            qr = pyqrcode.create('otpauth://totp/{label}?secret={secret}&issuer={issuer}'.\
                format(label=acc[7], secret=acc[2], issuer=acc[6]))
        else:
            qr = pyqrcode.create('otpauth://totp/{label}?secret={secret}'.\
                format(label=acc[7], secret=acc[2]))

        print(qr.terminal())
        input("Press Enter to continue...")

    sys.exit(0)

if __name__ == "__main__":
    main()
