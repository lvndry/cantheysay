from typing import Any
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request
from flask_cors import CORS

BASE_URL = "https://ethnicelebs.com"

app = Flask(__name__)
CORS(app)


def get_user(name: str):
    response = requests.get(
        BASE_URL + "/" + name.strip().replace(" ", "-").lower()
    )

    return response.text, response.status_code


def parse_data(html_text):
    soup = BeautifulSoup(html_text, 'lxml')

    # Looking for <strong><Ethnicity: .../strong>
    strongs = soup.find_all("strong")

    ethnicity = ""
    if len(strongs) > 0:
        for strong in strongs:
            if "ethnicity:" in str(strong).lower():
                ethnicity = str(strong).lower()
                break

    # Looking for tag african
    tags = soup.find("p", {"class": "post-tags"})
    return ethnicity, tags


def is_african(ethnicity: str, tags):
    african_tag = False
    if len(list(tags.children)) > 0:
        for child in tags.children:
            if "african" in str(child).lower():
                african_tag = True
                break

    return african_tag == True or "african" in ethnicity


@app.route('/search', methods=["POST"])
def main():
    name = request.json["name"]
    if len(name) == 0:
        return {
            "message": "You must type a correct name"
        }, 400

    can_they = False
    app.logger.info(f'Can {name} say the n-word?')

    data, status = get_user(name)
    if status == 404:
        return {}, 404
    ethnicity, tags = parse_data(data)
    if is_african(ethnicity, tags) == True:
        app.logger.info("Yes")
        can_they = True
    else:
        app.logger.info("No")

    return {
        "canthey": can_they
    }, 200


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3030)
    main()
