import string

linksToIgnore = ["https://play.google.com", "https://facebook.com", "https://twitter.com", "https://t.co", "https://web.whatsapp.com", "https://www.cloudflare.com", "https://youtube.com", "https://www.youtube.com", "https://instagram.com", "https://www.instagram.com", "https://charts.spotify.com", "https://www.tiktok.com", "mailto:", "https://api.whatsapp.com/send", "https://www.facebook.com", "https://telegram.me/share/url", "https:whatsapp", "https://twitter.com", "https://www.twitter.com", "https://www.linkedin.com", "https://www.pinterest.com", "https://www.reddit.com", "https://www.tumblr.com"]

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