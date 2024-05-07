
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import regex as re
from glob import glob


LEAGUE = "Bundesliga"
finished = [x.split("/")[-1][:-4] for x in glob("data/ClubAliasAll/*")]
print(finished[0])
df = pd.read_csv("data/all_transfers_no_duplicates_updated.csv")
leagues = set(df["From_League"]).union(set(df["To_League"]))
leagues.remove("-")

print("starting")
for league in tqdm(leagues):
    if league in finished:
        continue

    url = f"https://www.transfermarkt.com/bundesliga/ewigeTabelle/wettbewerb/{league}"
    response = requests.get(url)

    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': '_sp_v1_ss=1:H4sIAAAAAAAAAItWqo5RKimOUbKKxs_IAzEMamN1YpRSQcy80pwcILsErKC6lpoSSrEA-EAOLpYAAAA%3D; _sp_v1_p=619; _sp_v1_data=745500; _sp_su=false; euconsent-v2=CP855AAP855AAAGABCENAvEsAP_gAEPAAAZQJDgBdDJECCFAIXBTAOsQKIEVUVABAEAAAAABACABQAAAIAQCkAAAAACAAiAAARAAIEQAAAAAAAAABAAAAIAAIAAEAAAQgCAIIAAAAAAAAABAAAAIAAAAQAAAgAABAAQAkACIAAIAUEAAAAACAAAQAIAAAIAAAgAAAAAAAAAAAAIIICgAAAAAEAAAAAACABAAAAAIH7wEQAFAAOAEUAI4AcgBCACIgFiALqAa8A7YCwgF0AMEAZCAyYB-4BgSAoABUADgAIIAZABoAEQAJgAZgA3gB6AD8AIQAQwAmgBlAD9AUeAvMBkgDcwIXBQAQAigF0DoDIAFQAOAAggBkAGgARAAmQBcAF0AMQAZgA3gB6AD8AIYATQAygB-gEWALEAi8BR4CrAF5gMkAZYA4seABAEUOAAgNzIQBwAmABcADEAG8APQAjgFWEAAIA5CUAoADgARAAmABcADEAIYBF4CjwF5gMkJAAQGWFoAQAjgFWFICgAFQAOAAgABoAEQAJgAUgAxABmAD8AIYAZQA_QCLAHtAReAqwBeYDJAGWFAAgAMgAtgDkAbmAAA.YAAAAAAAAAAA; consentUUID=e017fa07-0534-4673-bef6-72bfdb860c8e_30; _pbjs_userid_consent_data=5250065792394867; kndctr_B21B678254F601E20A4C98A5_AdobeOrg_identity=CiY1NjI2MzE0ODU4NDY3MzE1NDY3MzM5NTkyOTA5NTkyMTEyMTY2NlITCMK3we3sMRABGAEqBElSTDEwAPAB-sjY8PQx; AMCV_B21B678254F601E20A4C98A5%40AdobeOrg=MCMID|56263148584673154673395929095921121666; _cc_id=b3130291efd590a3e4469b5e6c43eadd; __gads=ID=e87b16120b95a9cd:T=1712847872:RT=1715002749:S=ALNI_MYnLq1Z7SyUl40YVF55qcX1ssDjCA; __gpi=UID=00000deb17cdbb51:T=1712847872:RT=1715002749:S=ALNI_MYl0brbYPauvKZJzRv4WPCU7_fYAA; __eoi=ID=f30b96c390fe9167:T=1713453483:RT=1715002749:S=AA-AfjbVuBnYjTPhKf3mXxicmiQb; _pubcid=99184289-71a2-48b1-b907-574aabba50fb; pbjs-unifiedid=%7B%22TDID_LOOKUP%22%3A%22FALSE%22%2C%22TDID_CREATED_AT%22%3A%222024-05-06T13%3A29%3A36%22%7D; cto_bundle=e6JY_V80YmQySzJHM1MzVSUyQmh6a1FHRm41RDhYcWlFTGJmMXdPeG1sMk9IaXMxJTJCa2JMaHUlMkJYWlZOMWhKZm05RlBPOXN6dXdXdEVFMUVLTGprUnRxVTd0alBoR2xqTUQ4SGhvZHo3cXA4cXNvT2lrcnBHM3EwbDRuMXpDbmRrTEZBWkZaUQ; _lr_env_src_ats=false; pbjs-unifiedid_last=Mon%2C%2006%20May%202024%2013%3A33%3A22%20GMT; uuid=AC6960FF-0676-481B-9BC5-F71ED7A2FDF8; csuuidSekindo=6633a0b1dfa55; TMSESSID=a0bf70a22330d5d35d23cd45146b3a4a; kndctr_B21B678254F601E20A4C98A5_AdobeOrg_cluster=irl1; panoramaId_expiry=1715088428503; _lr_retry_request=true; cto_bidid=xPRf4l9kYlFDZkhLMWJWREJvTnlQVVZjNDVIU2R3UUsyUEh6TUxrMVliNG5iV1ElMkZZWkVtME1uaWhKVlNtZkMwSktIaHBVREtqQldLZXpuaVNGOWJoUk5DZ2hnJTNEJTNE',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers',
    }

    response = requests.get(url, headers=headers)


    
    # Check if the request was successful
    club_list = []

    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all("tbody")[1]
            for club in table.find_all("a"):
                if club.find("img"):
                    club_list.append({
                        "name" : club["title"],
                        "id" : club["href"].split("/")[1],
                        "logo_link" : re.sub("/tiny/", "/head/", club.img["src"])
                    })
            
            df = pd.DataFrame(club_list)
            df.to_csv(f"data/ClubAliasAll/{league}.csv", index=False)
        except:
            print(f"Error on: {league}")

    else:
        print(league)

