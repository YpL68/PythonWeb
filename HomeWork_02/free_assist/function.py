import re

ANSI_COLORS = {"red": "\x1b[91m", "blue": "\x1b[94m", "green": "\x1b[92m", "yellow": "\x1b[93m"}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

CYRILLIC_KEYS = "йцукенгшщзхъфывапролджэячсмитьбю"
TRANSLATION_KEYS = ("q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "a", "s", "d", "f",
                    "g", "h", "j", "k", "l", ";", "'", "z", "x", "c", "v", "b", "n", "m", ",", ".")


# translation table
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

TRANS_KEYS = {ord(c): l for c, l in zip(CYRILLIC_KEYS, TRANSLATION_KEYS)}


def normalize(src_str: str) -> str:
    return "_".join(re.findall(r"\w+", src_str.translate(TRANS)))


def highlight_str(src_str: str, text_color: str) -> str:
    return text_color + src_str + "\033[0;0m"


def match_highlight(match_str: str):
    pattern_str = "[()-]{,1}".join(list(match_str)) if match_str.isdecimal() else match_str.lower()
    pattern = re.compile(pattern_str, re.IGNORECASE)

    def inner(srs_str: str):
        tmp_list = pattern.split(srs_str)
        for item in enumerate(pattern.finditer(srs_str)):
            tmp_list[item[0]] = tmp_list[item[0]] + highlight_str(item[1].group(),  ANSI_COLORS["yellow"])
        return "".join(tmp_list)

    return inner


def easy_table(data, cell_sep=' | ', header_separator=True, highlight_math="") -> str:
    rows = len(data)
    cols = len(data[0])
    max_area_width = 80 - cols * 3
    col_max_width = int(max_area_width / cols)
    out_list = []

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        max_col_width = len(max(columns, key=len))
        col_width.append(max_col_width if max_col_width < col_max_width else col_max_width)

    free_size = max_area_width - sum(col_width)
    if free_size:
        col_trunc_qty = len([i for i in col_width if i == col_max_width])
        if col_trunc_qty:
            add_size = int(free_size / col_trunc_qty)
            for idx in range(len(col_width)):
                if col_width[idx] == col_max_width:
                    col_width[idx] += add_size

    separator = "-+-".join('-' * n for n in col_width)

    out_list.append(separator)
    for i, row in enumerate(range(rows)):
        if i == 1 and header_separator:
            out_list.append(separator)

        highlight_func = None
        if highlight_math:
            highlight_func = match_highlight(highlight_math)

        col_pos = [0] * cols
        while True:
            result = []
            for col in range(cols):
                idx_start = col_pos[col]
                idx_end = idx_start + col_width[col]
                sub_str = data[row][col][idx_start:idx_end+1].replace("\n", " ")
                if len(sub_str.rstrip()) > col_width[col]:
                    ind_spc = sub_str.rfind(" ")
                    if ind_spc != -1:
                        sub_str_t = sub_str[0:ind_spc]
                        if sub_str_t.strip():
                            sub_str = sub_str_t
                            idx_end = idx_start + len(sub_str) + 1  # fact
                        else:
                            sub_str = sub_str[0:col_width[col]]
                    else:
                        sub_str = sub_str[0:col_width[col]]
                    item = sub_str.strip().ljust(col_width[col])
                else:
                    item = sub_str.rstrip().ljust(col_width[col])

                if col == 0 and sub_str.strip().isdecimal():
                    item = sub_str.strip().rjust(col_width[col])
                if item:
                    if highlight_func:
                        item = highlight_func(item)
                result.append(item)
                col_pos[col] = idx_end
            if "".join(result).strip():
                out_list.append(cell_sep.join(result))
            else:
                break
    out_list.append(separator)
    return "\n".join(out_list)
