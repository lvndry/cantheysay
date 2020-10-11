import requests
import sys
from bs4 import BeautifulSoup
from flask import Flask
from flask import request

BASE_URL = "https://ethnicelebs.com"

app = Flask(__name__)


def get_user(name: str):
    response = requests.get(
        BASE_URL + "/" + name.strip().replace(" ", "-").lower())

    return response.text, response.status_code


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

    return african == True or "african" in ethnicity.lower()


@app.route('/search', methods=["POST"])
def main():
    name = request.json["name"]
    print(name)
    theyCan = False
    print("Can " + name + " say the n-word?")
    data, status = get_user(name)
    if status == 404:
        return {}, 404
    ethnicity, tags = parse_data(data)
    if is_african(ethnicity, tags) == True:
        print("Yes")
        theyCan = True
    else:
        print("No")

    return {
        "theycan": theyCan
    }, 200


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
    main()
