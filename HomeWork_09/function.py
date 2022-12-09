def format_phone_num(pn) -> str:
    return f"+{pn[:3]}({pn[3:5]}){pn[5:8]}-{pn[8:10]}-{pn[10:]}"
