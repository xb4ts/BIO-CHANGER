# FF BIO CHANGER

A lightweight Python tool for updating a FF player's social bio using an authenticated JWT request.

## Features

* Update your bio
* Supports multiple regions
* JWT Bearer authentication
* Simple interactive CLI

## Requirements

```bash
pip install requests pycryptodome
```

## Usage

```bash
python main.py
```

Enter:

```text
JWT: your_jwt
Region: ME
New Bio: Your new bio
```

Supported regions:

```text
IND
ME
BR
US
SAC
NA
```

## Output

Successful request:

```text
[+] Bio updated.
```

Failed request:

```text
[-] Request failed.
```

## Disclaimer

For educational and research purposes only. Use only with accounts and services you are authorized to access.
