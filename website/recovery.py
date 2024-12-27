from tkinter import Tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno, showinfo
from sqlalchemy import text
from . import APP
from .data import DB, RecoveryAuth, Password, add_model
from .crypt import KEY_FOLDER, encrypt_bytes, decrypt_bytes
from .temporary import SESSION_PSW
from .logic.updating.user import update_passwords
from .debugger import log

ROOT = Tk()
ROOT.withdraw()

RECOVERY_FILE = KEY_FOLDER / "RECOVERY"
RECOVERY_CRYPT = None


def set_recovery_crypt(psw):
    global RECOVERY_CRYPT
    RECOVERY_CRYPT = encrypt_bytes(psw, SESSION_PSW)


def check_existing_config():
    if not RecoveryAuth.query.all():
        log('warn', "No recovery codes found, requesting new ones...")

        auth_len = 0
        recovery_password = ""

        showinfo("Missing recovery codes",
                 "Missing recovery codes, we need at least 3.\n"
                 "Make sure to type in those codes by different persons.\n\n"
                 "Every person is needed for server session recovery!")

        while True:
            result = askstring(f"Recovery code {auth_len + 1}", "Enter recovery code: ")
            while not result or len(result) <= 8:
                result = askstring(f"Recovery code {auth_len + 1}", "Recovery code must be longer than 8 characters!\n"
                                                                "Enter recovery code: ")

            recovery_auth = RecoveryAuth(result)
            add_model(recovery_auth)
            auth_len += 1
            recovery_password += result

            if auth_len >= 3:
                result = askyesno("Enough recovery codes", "You have now enough codes to continue.\n"
                                                  "Do you want to create more?"
                                                  "- Will increase safety, but recovery is more complex.")

                if not result:
                    break

        showinfo("Recovery codes created", f"You have created {auth_len} recovery codes now.\n"
                 f"Never loose them - user data might be lost!")

        set_recovery_crypt(recovery_password)
        safe_session_password()
        log('info', "Recovery codes created.")

        return False

    return True


def safe_session_password():
    log('info', "Saving recovery file...")
    with open(RECOVERY_FILE, "wb") as f:
        recovery_psw = decrypt_bytes(RECOVERY_CRYPT, SESSION_PSW, True)
        f.write(encrypt_bytes(SESSION_PSW, recovery_psw))
    log('info', "Recovery file saved.")


def _request_recovery_psw():
    log('info', "Requesting recovery password...")
    recovery_password = ""

    for auth in RecoveryAuth.query.all():
        result = askstring(f"Recovery code {auth.id}", "Enter recovery code: ")
        while not result or not auth.check_psw(result):
            result = askstring(f"Recovery code {auth.id}", "Wrong recovery code!\n"
                                                           "Enter your code again: ")

        recovery_password += result

    return recovery_password


def start_recovery():
    user_psw_len = len(Password.query.all())
    if user_psw_len > 0 and RECOVERY_FILE.exists():
        recovery_password = _request_recovery_psw()

        with open(RECOVERY_FILE, "rb") as f:
            old_psw = decrypt_bytes(f.read(), recovery_password, True)
            update_passwords(old_psw)

    elif user_psw_len > 0 and not RECOVERY_FILE.exists():
        log('warn', "Missing recovery file, cannot recover session password.")
        showinfo("Missing recovery file", "Missing recovery file, cannot recover session password.")
        with DB.engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.execute(text("TRUNCATE TABLE EncryptedPassword"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        log('info', "User passwords not recoverable. Continuing...")
        recovery_password = _request_recovery_psw()

    else:
        log('info', "Nothing to recover...")
        recovery_password = _request_recovery_psw()

    set_recovery_crypt(recovery_password)
    safe_session_password()