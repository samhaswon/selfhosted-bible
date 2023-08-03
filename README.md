# [Self-hosted Bible](https://github.com/samhaswon/selfhosted-bible)
![An icon with the letters S, H, and B on a black background.](static/favicon.svg "Logo")
A self-hosted webapp of various Bible versions including the KJV, ESV, and ASV.

## Supported Architectures
| Architecture | Available | Tag    |
|:------------:|:---------:|--------|
|    x86-64    |     ✅     | latest |
|   arm64v8    |     ✅     | latest |

## Examples
*Note: Screen shots taken in dark mode <br>
### Home page
![Home page image](pictures/home.jpg)
### Single version reading
![Example view of using a single version. The passage is Genesis chapter 1](pictures/single_version.jpg)
### Split version reading
![Example image of two versions side by side. The example is using the ESV and KJV for the passage Genesis chapter 1](pictures/split_version.jpg)

# Instructions

## Generating an API key for authorized ESV access:
To start, make an account at [esv.org](https://www.esv.org/). After creating an account at 
[esv.org](https://www.esv.org/), create an API key at 
[https://api.esv.org/account/create-application/](https://api.esv.org/account/create-application/). Then place the key 
in [esv-api-key.txt](esv-api-key.txt) in place of "\<key-goes-here\>" for local installation or save the key for later 
if running in Docker.

## Running the application
<details>
    <summary>Locally</summary>

#### *Install Python 3*
This application requires Python 3 to run. To install it on Windows, download and run the installer at 
[python.org](https://www.python.org/downloads/). For Linux installation, you likely already have Python installed but 
maybe not pip. In this case, install python3 (if not already installed) and py3-pip (or whatever the package name is for 
Python 3 pip in your package manager) through your package manager. <br><br>
Then, verify Python was installed by running `python3 --version` on Linux or `py -version` on Windows.

For more detailed installation instructions, see [realpython.com](https://realpython.com/installing-python/).

#### *Install requirements*
```shell
pip3 install -r requirements.txt
```
#### *Execute:*
```shell
waitress-serve --port=5000 --call "main:create_app"
```
</details>

<details>
    <summary>In Docker</summary>

With docker, you have 2 options. You can either build the container yourself or pull it from 
[docker hub](https://hub.docker.com/r/samhaswon/self-hosted-bible)
#### Build the container
If you choose this option, replace `samhaswon/self-hosted-bible:latest` with `self-hosted-bible` in the Docker run 
command or Docker compose file.
```shell
docker build -t self-hosted-bible .
``` 
##### (or) Pull the container
```shell
docker pull samhaswon/self-hosted-bible:latest
```

##### Run the container (detached)
**Note** The volume, `/usr/src/app/bibles/json-bibles` is to give the container a persistent cache between versions <br><br>
Docker run
```shell
docker run -dp 5000:5000 \
       --restart=always \
       --name self-hosted-bible \
       -e ESV_API_KEY=<key-goes-here> \
       -v <host_path>:/usr/src/app/bibles/json-bibles
       samhaswon/self-hosted-bible:latest
```
Docker compose
```yaml
version: '3'
services:
  self-hosted-bible-server:
    image: samhaswon/self-hosted-bible:latest
    container_name: self-hosted-bible
    ports:
      - "5000:5000"
    restart: always
    volumes:
      - /path/to/json/bibles:/usr/src/app/bibles/json-bibles
    environment:
      - ESV_API_KEY=<key-goes-here>
```
</details>

## *Navigate to the webpage*
To access a locally hosted version of the application, go to [localhost:5000](http://localhost:5000) or 
[127.0.0.1:5000](http://127.0.0.1:5000). To access the application running in Docker on another machine, go to 
<machine_ip>:5000 .

## Copyright Notice:
The code included in this repository is subject to the included license, but the content from external sources is not.

<details>
    <summary>AMP Notice</summary>

> Scriptures marked AMP are taken from the AMPLIFIED BIBLE (AMP): Scripture taken from the AMPLIFIED® BIBLE, Copyright 
> © 1954, 1958, 1962, 1964, 1965, 1987 by the Lockman Foundation Used by Permission. 
> (<a href="https://www.lockman.org/">www.Lockman.org</a>)
</details>

<details>
    <summary>ASV Notice</summary>

> Scripture quotations marked “ASV” are taken from the American Standard Version Bible (Public Domain).
</details>

<details>
    <summary>BSB Notice</summary>

> The Holy Bible, Berean Standard Bible, BSB is produced in cooperation with <a href="//biblehub.com">Bible Hub</a>, 
> <a href="//discoverybible.com">Discovery Bible</a>, <a href="//openbible.com">OpenBible.com</a>, and the Berean Bible 
> Translation Committee. This text of God's Word has been <a href="https://creativecommons.org/publicdomain/zero/1.0/"> 
> dedicated to the public domain</a>.
</details>

<details>
    <summary>CSB Notice</summary>

> Scripture quotations marked CSB have been taken from the Christian Standard Bible®, Copyright © 2017 by Holman Bible 
> Publishers. Used by permission. Christian Standard Bible® and CSB® are federally registered trademarks of Holman Bible 
> Publishers.
</details>

<details>
    <summary>ESV Notice</summary>

>Scripture quotations marked “ESV” are from the ESV® Bible (The Holy Bible, English Standard Version®), copyright © 2001 
> by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved. The ESV text may 
> not be quoted in any publication made available to the public by a Creative Commons license. The ESV may not be 
> translated into any other language.
>
>Users may not copy or download more than 500 verses of the ESV Bible or more than one half of any book of the ESV Bible.
</details>

<details>
    <summary>GNV Notice</summary>

Geneva Bible (1599)
> This digital copy is freely available world-wide, with no copyright restrictions, courtesy of eBible.org and many others.
</details>

<details>
    <summary>KJV Notice</summary>

> Rights in The Authorized Version of the Bible (King James Bible) in the United Kingdom are vested in the Crown and 
> administered by the Crown’s patentee, Cambridge University Press. The reproduction by any means of the text of the 
> King James Version is permitted to a maximum of five hundred (500) verses for liturgical and non-commercial 
> educational use, provided that the verses quoted neither amount to a complete book of the Bible nor represent 25 per 
> cent or more of the total text of the work in which they are quoted, subject to the following acknowledgement being 
> included:
> 
> Scripture quotations from The Authorized (King James) Version. Rights in the Authorized Version in the United Kingdom 
> are vested in the Crown. Reproduced by permission of the Crown’s patentee, Cambridge University Press
> When quotations from the KJV text are used in materials not being made available for sale, such as church bulletins, 
> orders of service, posters, presentation materials, or similar media, a complete copyright notice is not required but 
> the initials KJV must appear at the end of the quotation.
> Rights or permission requests (including but not limited to reproduction in commercial publications) that exceed the 
> above guidelines must be directed to the Permissions Department, Cambridge University Press, University Printing 
> House, Shaftesbury Road, Cambridge CB2 8BS, UK (https://www.cambridge.org/about-us/rights-permissions) and approved 
> in writing.
</details>

<details>
    <summary>LSV Notice</summary>

> Scripture quotations marked “LSV” are taken from the Literal Standard Version (Creative Commons Attribution-ShareAlike 
> license). See more <a href="https://www.lsvbible.com/">here</a> 
</details>

<details>
    <summary>MSG Notice</summary>

> Scripture quotations marked "MSG" are from THE MESSAGE. Copyright © by Eugene H. Peterson 1993, 2002, 2005, 2018. Used 
> by permission of NavPress. All rights reserved. Represented by Tyndale House Publishers, Inc. 
</details>

<details>
    <summary>NASB (1995) Notice</summary>

> Scripture quotations taken from the (NASB®) New American Standard Bible®, Copyright © 1960, 1971, 1977, 1995 by The 
> Lockman Foundation. Used by permission. All rights reserved. <a href="lockman.org">lockman.org</a>
</details>

<details>
    <summary>NET Notice</summary>

> The Scriptures quoted are from the NET Bible® https://netbible.com copyright ©1996, 2019 used with permission from 
> Biblical Studies Press, L.L.C. All rights reserved
>
> To see the NET Bible® study tool go to https://netbible.org.
</details>

<details>
    <summary>NIV Notice</summary>

> The Holy Bible, New International Version®, NIV® Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.® Used with 
> permission. All rights reserved worldwide.
</details>

<details>
    <summary>NKJV Notice</summary>

> Scriptures marked NKJV are taken from the NEW KING JAMES VERSION (NKJV): Scripture taken from the NEW KING JAMES 
> VERSION®. Copyright© 1982 by Thomas Nelson, Inc. Used by permission. All rights reserved. 

<a href="https://www.thomasnelson.com/about-us/permissions/#permissionBiblesmartphone">See more info about usage of the NKJV here</a>
</details>

<details>
    <summary>NLT Notice</summary>

> Scriptures marked NLT are taken from the HOLY BIBLE, NEW LIVING TRANSLATION (NLT): Scriptures taken from the HOLY 
> BIBLE, NEW LIVING TRANSLATION, Copyright© 1996, 2004, 2007 by Tyndale House Foundation. Used by permission of Tyndale 
> House Publishers, Inc., Carol Stream, Illinois 60188. All rights reserved. Used by permission.
</details>

<details>
    <summary>RSV Notice</summary>

> Scriptures marked RSV are taken from the REVISED STANDARD VERSION (RSV): Scripture taken from the REVISED STANDARD 
> VERSION, Grand Rapids: Zondervan, 1971.
</details>

<details>
    <summary>WEB Notice</summary>

- Note: Only canonical books available
> Scriptures marked WEB are taken from THE WORLD ENGLISH BIBLE (WEB): WORLD ENGLISH BIBLE, public domain.
</details>

<details>
    <summary>YLT Notice</summary>

> Scripture quotations marked “YLT” are taken from The Young’s Literal Translation Bible (Public Domain).
</details>

## Credits
Credit to [@bibleapi](https://github.com/bibleapi/bibleapi-bibles-json) for KJV and ASV original JSON
