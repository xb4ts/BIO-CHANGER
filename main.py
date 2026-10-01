import sys
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def encode_varint(val: int) -> bytes:
    res = bytearray()
    while val >= 0x80:
        res.append((val & 0x7F) | 0x80)
        val >>= 7
    res.append(val & 0x7F)
    return bytes(res)

def build_payload(bio: str) -> bytes:
    bio_bytes = bio.encode("utf-8")

    raw_proto = b"\x10\x11\x2a\x00\x32\x00\x42"
    raw_proto += encode_varint(len(bio_bytes))
    raw_proto += bio_bytes
    raw_proto += b"\x48\x01\x5a\x00\x62\x00"

    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    encrypted = cipher.encrypt(pad(raw_proto, AES.block_size))
    return encrypted

def update_bio(jwt: str, region: str, bio: str) -> bool:
    urls = {
        "IND": "https://client.ind.freefiremobile.com/UpdateSocialBasicInfo",
        "BR": "https://client.us.freefiremobile.com/UpdateSocialBasicInfo",
        "US": "https://client.us.freefiremobile.com/UpdateSocialBasicInfo",
        "SAC": "https://client.us.freefiremobile.com/UpdateSocialBasicInfo",
        "NA": "https://client.us.freefiremobile.com/UpdateSocialBasicInfo",
    }
    url = urls.get(region.upper(), "https://clientbp.ppmainecoonghj.com/UpdateSocialBasicInfo")
    host = url.split("//", 1)[1].split("/", 1)[0]

    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.12f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB55",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A305F Build/RP1A.200720.012)",
        "Host": host,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }

    res = requests.post(url, headers=headers, data=build_payload(bio), timeout=15)
    
    if res.status_code != 200:
        print(f"[!] Error: {res.status_code}")
        print(f"[!] Body: {res.text}")
        
    return res.status_code == 200

if __name__ == "__main__":
    jwt = input("JWT: ").strip()
    region = input("Region: ").strip()
    bio = input("New Bio: ").strip()

    if not jwt or not bio:
        sys.exit(1)

    if update_bio(jwt, region, bio):
        print("[+] Bio updated.")
    else:
        print("[-] Request failed.")
