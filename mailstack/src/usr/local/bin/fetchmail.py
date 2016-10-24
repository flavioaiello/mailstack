#!/usr/bin/env python

import sqlite3
import time
import os
import tempfile
import shlex
import subprocess


FETCHMAIL = """
fetchmail -N \
    --sslcertck --sslcertpath /etc/ssl/certs \
    -f {}
"""


RC_LINE = """
poll "{host}" proto {protocol} port {port}
    user "{username}" password "{password}"
    smtphost "smtp"
    smtpname "{user_email}"
    {options}
"""


def escape_rc_string(arg):
    return arg.replace("\\", "\\\\").replace('"', '\\"')


def fetchmail(fetchmailrc):
    with tempfile.NamedTemporaryFile() as handler:
        handler.write(fetchmailrc.encode("utf8"))
        handler.flush()
        command = FETCHMAIL.format(shlex.quote(handler.name))
        output = subprocess.check_output(command, shell=True)
        return output


def run(connection, cursor):
    cursor.execute("""
        SELECT user_email, protocol, host, port, tls, username, password
        FROM fetch
    """)
    for line in cursor.fetchall():
        fetchmailrc = ""
        user_email, protocol, host, port, tls, username, password = line
        options = "options ssl" if tls else ""
        fetchmailrc += RC_LINE.format(
            user_email=escape_rc_string(user_email),
            protocol=protocol,
            host=escape_rc_string(host),
            port=port,
            username=escape_rc_string(username),
            password=escape_rc_string(password),
            options=options
        )
        try:
            print(fetchmail(fetchmailrc))
            error_message = ""
        except subprocess.CalledProcessError as error:
            error_message = error.output.decode("utf8")
            print(error.output)
        finally:
            cursor.execute("""
                UPDATE fetch SET error=?, last_check=datetime('now')
                WHERE user_email=?
            """, (error_message.split("\n")[0], user_email))
            connection.commit()



if __name__ == "__main__":
    db_path = os.environ.get("DB_PATH", "/database/mailstack.db")
    connection = sqlite3.connect(db_path)
    while True:
        time.sleep(int(os.environ.get("FETCHMAIL_DELAY", 10)))
        cursor = connection.cursor()
        run(connection, cursor)
        cursor.close()
