import requests
import sys
from bs4 import BeautifulSoup

BASE_URL = "https://ethnicelebs.com"


def get_user(name: str):
    response = requests.get(
        BASE_URL + "/" + name.strip().replace(" ", "-").lower())
    if response.status_code == 404:
        raise ValueError("User not found")

    return response.text


def parse_data(html_text):
    soup = BeautifulSoup(html_text, 'lxml')

    # Looking for <strong><Ethnicity: .../strong>
    strongs = soup.find_all("strong")

    ethnicity = ""
    if len(strongs) > 0:
        for strong in strongs:
            if "ethnicity:" in str(strong).lower():
                ethnicity = str(strong)
                break

    # Looking for tag african
    tags = soup.find("p", {"class": "post-tags"})
    return ethnicity, tags


def is_african(ethnicity: str, tags):
    african = False
    for child in tags.children:
        if "african" in str(child).lower():
            african = True
        break

    if african == True or "african" in ethnicity.lower():
        return True
    else:
        return False


def main():
    name = sys.argv[1]
    print("Can " + name + " say the n-word?")
    data = get_user(name)
    ethnicity, tags = parse_data(data)
    theycan = is_african(ethnicity, tags)
    if theycan == True:
        print("Yes")
    else:
        print("No")
    return


if __name__ == "__main__":
    main()
