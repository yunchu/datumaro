# Copyright (C) 2023 Intel Corporation
#
# SPDX-License-Identifier: MIT

import logging as log
from typing import Optional, Union

from cryptography.fernet import Fernet, InvalidToken


class Crypter:
    FERNET_KEY_LEN = 44

    def __init__(self, key: Union[str, bytes]) -> None:
        if isinstance(key, str):
            key = key.encode()
        self._key = key
        self._fernet = Fernet(self._key)

    @property
    def key(self) -> bytes:
        return self._key

    def decrypt(self, msg: bytes) -> bytes:
        return self._fernet.decrypt(msg)

    def encrypt(self, msg: bytes) -> bytes:
        return self._fernet.encrypt(msg)

    def handshake(self, key: bytes) -> bool:
        try:
            return self.decrypt(key) == self._key
        except InvalidToken as e:
            log.debug(e)
            return False

    @staticmethod
    def gen_key(key: Optional[bytes] = None) -> bytes:
        """If "key" is not None, return the different key with "key"."""
        _key = Fernet.generate_key()
        while _key == key:
            _key = Fernet.generate_key()
        return _key

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Crypter):
            return False

        return self._key == __o._key

    @property
    def is_null_crypter(self):
        return self == NULL_CRYPTER


class NullCrypter(Crypter):
    def __init__(self) -> None:
        self._key = None
        self._fernet = None

    def decrypt(self, msg: bytes) -> bytes:
        return msg

    def encrypt(self, msg: bytes) -> bytes:
        return msg

    def handshake(self, key: bytes) -> bool:
        return self.decrypt(key) == b""


NULL_CRYPTER = NullCrypter()
