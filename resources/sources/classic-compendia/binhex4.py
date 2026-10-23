"""Decode BinHex 4.0 (.hqx) files, the Macintosh archive format Bristol used for
FR2 in the 1990s. Python's binhex module was removed in 3.11; binascii.crc_hqx remains.

decode(raw_bytes) -> (name, file_type, creator, data_fork, resource_fork), after
checking the header and both fork CRCs (CRC-16/XMODEM).
"""

import binascii
import struct

ALPHABET = b"!\"#$%&'()*+,-012345689@ABCDEFGHIJKLMNPQRSTUVXYZ[`abcdefhijklmpqr"
VALUE = {c: i for i, c in enumerate(ALPHABET)}


def _six_bit(raw):
    start = raw.index(b"(This file must be converted with BinHex")
    body = raw[raw.index(b":", start) + 1:]
    out, acc, bits = bytearray(), 0, 0
    for c in body:
        if c == ord(":"):
            return bytes(out)
        if c in b"\r\n\t ":
            continue
        acc = (acc << 6) | VALUE[c]
        bits += 6
        if bits >= 8:
            bits -= 8
            out.append((acc >> bits) & 0xFF)
            acc &= (1 << bits) - 1
    raise ValueError("no closing colon")


def _unrle(data):
    out, i = bytearray(), 0
    while i < len(data):
        b = data[i]
        if b == 0x90:
            n = data[i + 1]
            i += 2
            if n == 0:
                out.append(0x90)
            else:
                out.extend(out[-1:] * (n - 1))
            continue
        out.append(b)
        i += 1
    return bytes(out)


def _crc_ok(block, stored):
    return binascii.crc_hqx(block, 0) == stored


def decode(raw):
    d = _unrle(_six_bit(raw))
    n = d[0]
    name = d[1:1 + n].decode("mac_roman")
    p = 1 + n + 1
    ftype, creator = d[p:p + 4], d[p + 4:p + 8]
    dlen, rlen = struct.unpack(">II", d[p + 10:p + 18])
    hend = p + 18
    if not _crc_ok(d[:hend], struct.unpack(">H", d[hend:hend + 2])[0]):
        raise ValueError(f"{name}: header CRC mismatch")
    ds = hend + 2
    data = d[ds:ds + dlen]
    if not _crc_ok(data, struct.unpack(">H", d[ds + dlen:ds + dlen + 2])[0]):
        raise ValueError(f"{name}: data fork CRC mismatch")
    rs = ds + dlen + 2
    rsrc = d[rs:rs + rlen]
    if not _crc_ok(rsrc, struct.unpack(">H", d[rs + rlen:rs + rlen + 2])[0]):
        raise ValueError(f"{name}: resource fork CRC mismatch")
    return name, ftype.decode("mac_roman"), creator.decode("mac_roman"), data, rsrc
