"""Run locally; paste only the resulting hash into Streamlit secrets."""
from getpass import getpass
from portrait_core import hash_password

if __name__ == '__main__':
    password = getpass('Neues Zugangspasswort (mindestens 4 Zeichen): ')
    if len(password) < 4:
        raise SystemExit('Bitte mindestens 4 Zeichen verwenden.')
    if password != getpass('Passwort wiederholen: '):
        raise SystemExit('Die Eingaben stimmen nicht überein.')
    print('APP_PASSWORD_HASH = "' + hash_password(password) + '"')
