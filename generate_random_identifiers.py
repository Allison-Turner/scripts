#! /usr/bin/env python3

import datetime
import random
import ipaddress
import uuid

# from https://gist.github.com/pklaus/9638536?permalink_comment_id=2887047#gistcomment-2887047
def generate_random_mac():
    return ':'.join('%02x'%random.randrange(256) for _ in range(6))


# from https://stackoverflow.com/a/21014713
def generate_random_ipv4_address():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


# from https://stackoverflow.com/a/21018897
def generate_random_ipv6_address():
    return str(ipaddress.IPv6Address(random.randint(0, 2**128-1)))


def generate_random_duid():
    duid_type = random.randint(1, 4)

    # DUID-LLT
    if duid_type == 1:
        duid_type_str = "00:01"
        mac = generate_random_mac()

        hw_type = random.randint(0,65535)
        hw_type_byte_1, hw_type_byte_2 = hex(hw_type >> 8).replace("0x", ""), hex(hw_type & 0xFF).replace("0x", "")

        if len(hw_type_byte_1) < 2:
            hw_type_byte_1 = "0" + hw_type_byte_1

        if len(hw_type_byte_2) < 2:
            hw_type_byte_2 = "0" + hw_type_byte_2

        ts_int = int((datetime.datetime.now() - datetime.datetime(2000, 1, 1)).total_seconds())
        ts_hex = hex(ts_int).replace("0x", "")
        if len(ts_hex) % 2 != 0:
            ts_hex = "0" + ts_hex
        ts_octs = [ts_hex[i:i+2] for i in range(0, len(ts_hex), 2)]
        ts = ':'.join(ts_octs)

        return '{}:{}:{}:{}:{}'.format(duid_type_str, hw_type_byte_1, hw_type_byte_2, ts, mac)

    # DUID-EN
    elif duid_type == 2:
        duid_type_str = "00:02"
        
        # https://www.iana.org/assignments/enterprise-numbers/enterprise-numbers
        en = random.randint(0, 59229)
        en_byte_1, en_byte_2 = hex(en >> 8).replace("0x", ""), hex(en & 0xFF).replace("0x", "")

        if len(en_byte_1)  < 2:
            en_byte_1 = "0" + en_byte_1

        if len(en_byte_2)  < 2:
            en_byte_2 = "0" + en_byte_2

        en_str = '{}:{}'.format(en_byte_1, en_byte_2)

        en_id_segments = []
        id_len = random.randint(2, 32)

        for x in range(id_len):
            num = hex(random.randint(0,255)).replace("0x", "")

            if len(num) < 2:
                num = "0" + num
            en_id_segments.append(num)

        en_id_str = ':'.join(en_id_segments)

        return '{}:{}:{}'.format(duid_type_str, en_str, en_id_str)
            
    # DUID-LL
    elif duid_type == 3:
        duid_type_str = "00:03"
        mac = generate_random_mac()

        hw_type = random.randint(0,65535)
        hw_type_byte_1, hw_type_byte_2 = hex(hw_type >> 8).replace("0x", ""), hex(hw_type & 0xFF).replace("0x", "")

        if len(hw_type_byte_1) < 2:
            hw_type_byte_1 = "0" + hw_type_byte_1

        if len(hw_type_byte_2) < 2:
            hw_type_byte_2 = "0" + hw_type_byte_2

        return '{}:{}:{}:{}'.format(duid_type_str, hw_type_byte_1, hw_type_byte_2, mac)

    # DUID-UUID
    elif duid_type == 4:
        duid_type_str = "00:04"

        octets = []

        for i in range(16):
            hex_num_1 = hex(random.randint(0,15)).replace("0x", "")
            hex_num_2 = hex(random.randint(0,15)).replace("0x", "")

            octet = hex_num_1 + hex_num_2
            octets.append(octet)

        # TODO: use uuid module instead

        return '{}:{}'.format(duid_type_str, ':'.join(octets))
