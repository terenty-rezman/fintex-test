
DIR = "./downloads"

list = [
    {
        "alias": "google_page",
        "url": "https://www.google.com"
    },
    {
        "alias": "network_book",
        "url": "https://github.com/AnnAsmoothsea/Computer-Networking-A-Top-Down-Approach-6th-Edition/raw/master/Computer%20Networking%20A%20Top-Down%20Approach%206th%20E.pdf"
    }
][1:2]

aliases = {item["alias"] for item in list}

urls = {item["alias"]: item["url"] for item in list}
