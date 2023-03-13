# Self-hosted Bible
A self-hosted webapp of various Bible versions including the KJV, ESV, and ASV.

# Instructions

## Generating an API key for authorized ESV access:
The ESV API may be used unauthorized, but it is recommended to use it authorized to avoid issues. <br><br>
To start, make an account at [esv.org](https://www.esv.org/). After creating an account at [esv.org](https://www.esv.org/), create an API key at [https://api.esv.org/account/create-application/](https://api.esv.org/account/create-application/). Then place the key in [api-key.txt](api-key.txt) in place of "<key-goes-here>".

## Running the application
<details>
    <summary>Locally</summary>

#### *Install requirements*
```sh
pip3 install -r requirements.txt
```
#### *Execute:*<br>
*(Linux / Mac)*
```sh
python3 main.py
```
or<br>
*Windows*
```ps
py main.py
```
</details>

<details>
    <summary>In Docker</summary>

#### Building the container
```sh
docker build -t self-hosted-bible .
``` 

#### Run the container (detached)
```sh
docker run -dp 5000:5000 --restart=always --name self-hosted-bible -e API_KEY=key self-hosted-bible
```
</details>

## *Navigate to the webpage*
To access a locally hosted version of the application, go to [localhost:5000](http://localhost:5000) or [127.0.0.1:5000](http://127.0.0.1:5000)

## Copyright Notice:
The code included in this repository is subject to the included license, but the content from external sources is not.

<details>
    <summary>ESV Notice</summary>

>Scripture quotations marked “ESV” are from the ESV® Bible (The Holy Bible, English Standard Version®), copyright © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved. The ESV text may not be quoted in any publication made available to the public by a Creative Commons license. The ESV may not be translated into any other language.
>
>Users may not copy or download more than 500 verses of the ESV Bible or more than one half of any book of the ESV Bible.
</details>

## Other Credits
Credit to [@bibleapi](https://github.com/bibleapi/bibleapi-bibles-json) for KJV and ASV original JSON
