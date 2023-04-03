import string

linksToIgnore = ["https://www.instagram.com", "https://charts.spotify.com", "https://www.tiktok.com", "mailto:", "https://api.whatsapp.com/send", "https://www.facebook.com/sharer/sharer.php", "https://telegram.me/share/url", "https:whatsapp", "https://www.facebook.com/dialog/feed"]

def clearLinks(dirtyLinks: list, fromLink: str = None):
    cleanLinks = list()
    for link in dirtyLinks:
        if link != None and link:
            if link == "#":
                continue
            
            link.strip()
            
            ignore = False
            
            for z in linksToIgnore:
                if link.startswith(z):
                    ignore = True
                    break
            
            if ignore == False:
                if link.startswith("https:") or link.startswith("http:"):
                    cleanLinks.append(link)
                elif link[0] == " ":
                    cleanLinks.append(link[1:])
                else:
                    if link != "/":
                        if link[0] == "/":
                            if link[1] in list(string.ascii_letters) and fromLink != None:
                                cleanLinks.append(fromLink+link)
                        else:
                            if link[0] != "#":
                                cleanLinks.append("https:"+link)
    return cleanLinks