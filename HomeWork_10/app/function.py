import re


def format_phone_num(pn: str) -> str:
    return f"+{pn[:3]}({pn[3:5]}){pn[5:8]}-{pn[8:10]}-{pn[10:]}"


def sanitize_phone_num(pn: str) -> str:
    tel_code = {9: "380", 10: "38"}
    snz_phone = "".join([ch for ch in pn if ch.isdecimal()])
    if len(snz_phone) not in (9, 10, 12):
        raise ValueError(f"Entered phone '{pn}' is incorrect.")
    return tel_code.get(len(snz_phone), "") + snz_phone


def email_validate(email: str):
    if email:
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.fullmatch(regex, email):
            raise ValueError(f"Entered email '{email}' is incorrect.")
