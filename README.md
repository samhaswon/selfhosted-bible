# ESV-WEB
A self-hosted webapp connecting to Crossway's ESV API

# Instructions

## Generating a key:
After creating an account at [esv.org](https://www.esv.org/), create an API key at [https://api.esv.org/account/create-application/](https://api.esv.org/account/create-application/). Then place the key in [api-key.txt](api-key.txt) in place of "<key-goes-here>".

## Running the application locally
#### *Install requirements*
```bash
pip3 install -r requirements.txt
```
#### *Execute:*<br>
*(Linux / Mac)*
```bash
python3 main.py
```
or<br>
*Windows*
```ps
py main.py
```
#### *Navigate to the webpage*
To access a locally hosted version of the application, go to [localhost:5080](http://localhost:5080) or [127.0.0.1:5080](http://127.0.0.1:5080)

## Copyright Notice:
The code included in this repository is subject to the included license, but the content from external sources is not.

*ESV*:
>Scripture quotations marked “ESV” are from the ESV® Bible (The Holy Bible, English Standard Version®), copyright © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved. The ESV text may not be quoted in any publication made available to the public by a Creative Commons license. The ESV may not be translated into any other language.
>
>Users may not copy or download more than 500 verses of the ESV Bible or more than one half of any book of the ESV Bible.