import bibtexparser
import operator

# file name of the publication page
path = "./_pages/"
filename = path + "publications.md"

# header of the markdown file
header = """---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---
"""

# dictionary for the jornal abbreviation
journal_dict = {
    r"\apj" : {"name": "The Astrophysical Jornal", "abbr": "ApJ"},
    r"\aj"  : {"name": "The Astronomical Jornal", "abbr": "AJ"},
    r"\apjs": {"name": "The Astrophysical Jornal Supplement Series", "abbr": "ApJS"},
}

# special characters that should be replaced in markdown; you can freely add any characters as needed
special_chr = {
    r"\o": "&oslash;",
    r"\'a": "&aacute;",
    r"\'e": "&eacute;",
    r"\'\i": "&iacute;",
    r"\'o": "&oacute;",
    r"\"O": "&Ouml;",
    r"~": " "
}

# functions for generating markdown string
def format_author_name(author_name):
    family_name, first_name = author_name.split(", ")
    family_name = family_name.strip(r"{}")
    
    middle_name = ""
    if " " not in first_name or "(" in first_name:
        first_name_abbr = first_name[0] + "."
    else:
        first_name, middle_name = first_name.split(" ")
        if "." not in middle_name:
            middle_name = middle_name[0] + "."

    if "-" in first_name:
        first_name_abbr = first_name.split("-")[0][0] + ".-" + first_name.split("-")[1][0] + "."
    else:
        first_name_abbr = first_name[0] + "."
    
    return (family_name + ", " + first_name_abbr + " " + middle_name).strip()
        

def sort_entries(entries, reverse=False):
    return sorted(entries, key=operator.itemgetter('year', 'volume', "pages"), reverse=reverse)

def generate_reference_list(entries):
    str_list = []
    entries = sort_entries(entries=entries, reverse=True)
    for i, entry in enumerate(entries):
        index = len(entries) - i
        string = f"{index}\. "

        # title with hyper link to ads
        title = entry["title"].strip(r"{}")
        link = entry["adsurl"]
        string += f"[{title}]({link})  \n"

        # authors
        author_list = entry["author"].split(" and ")
        author_list_formatted = [format_author_name(name) for name in author_list]
        author_str = ", ".join(["**" + name + "**" if "Yamato, Y." in name else name for name in author_list_formatted])
        for chr in special_chr.keys():
            author_str = author_str.replace(chr, special_chr[chr])
        string += author_str + "  \n"

        # year
        string += entry["year"] + ", "

        # journal
        string += journal_dict[entry["journal"]]["name"] + ", "

        # volume and page
        string += entry["volume"] + ", " + entry["pages"]

        # new line
        string += "\n\n"

        # remove {}
        string = string.replace(r"{", "").replace(r"}", "")

        str_list.append(string)
    
    return str_list

if __name__ == "__main__":
    to_write = []

    to_write.append(header + "\n\n")

    # publication with significant contribution
    to_write.append("## Refereed Publications with Significant Contributions\n\n")

    with open(path + "leadauthor.bib", "r") as f:
        library = bibtexparser.load(f)

    ref_list = generate_reference_list(library.entries)

    to_write.extend(ref_list)

    # co-authored
    to_write.append("## Co-authored Refereed Publications\n\n")

    with open(path + "coauthored.bib", "r") as f:
        library = bibtexparser.load(f)

    ref_list = generate_reference_list(library.entries)

    to_write.extend(ref_list)

    with open(filename, "w") as f:
        f.writelines(to_write)
