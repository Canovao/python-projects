import string

def clearLinks(fromLink: str, dirtyLinks: list):
    cleanLinks = list()
    for link in dirtyLinks:
        if link != None and link:
            if link == "#":
                continue
            
            link.strip()
            
            if link.startswith("https:") or link.startswith("http:"):
                cleanLinks.append(link)
            elif link[0] == " ":
                cleanLinks.append(link[1:])
            else:
                if link != "/":
                    if link[0] == "/":
                        if link[1] in list(string.ascii_letters):
                            cleanLinks.append(fromLink+link)
                    else:
                        if link[0] != "#":
                            cleanLinks.append("https:"+link)
    return cleanLinks