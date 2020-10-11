# Can they say it ? - Server

## scrapper.py

```bash
# Terminal 1
$ python scrapper.py

# Terminal 2
$ curl --location --request POST 'http://localhost:3030/search' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "jason derulo"
}'

Can jason derulo say the n-word?
Yes

$ curl --location --request POST 'http://localhost:3030/search' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "rita ora"
}'

Can Rita Ora say the n-word?
No
```
