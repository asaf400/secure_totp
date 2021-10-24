from tinydb.storages import JSONStorage,touch
from utils.encryption import Encryption
from typing import Dict, Any, Optional
import os
import json
import io

class EncryptedJSONStorage(JSONStorage):
    """
    Store the data in a JSON file.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(access_mode='rb+',*args, **kwargs)
        self.encryptor=Encryption().encryptor

    def close(self) -> None:
        self._handle.close()

    def read(self) -> Optional[Dict[str, Dict[str, Any]]]:
        # Get the file size by moving the cursor to the file end and reading
        # its location
        self._handle.seek(0, os.SEEK_END)
        size = self._handle.tell()

        if not size:
            # File is empty so we return ``None`` so TinyDB can properly
            # initialize the database
            return None
        else:
            # Return the cursor to the beginning of the file
            self._handle.seek(0)

            # Ask the encryptor to decrypt the entire data pack
            data = self.encryptor.decrypt(self._handle.read())

            # Load the JSON contents of the file
            return json.loads(data)

    def write(self, data: Dict[str, Dict[str, Any]]):
        # Move the cursor to the beginning of the file just in case
        self._handle.seek(0)

        # Serialize the database state using the user-provided arguments
        serialized = json.dumps(data, **self.kwargs)

        # Write the serialized data to the file
        try:
            # Ask the encryptor to decrypt the entire data pack
            data = self.encryptor.encrypt(serialized)
            self._handle.write(data)
        except io.UnsupportedOperation:
            raise IOError('Cannot write to the database. Access mode is "{0}"'.format(self._mode))

        # Ensure the file has been writtens
        self._handle.flush()
        os.fsync(self._handle.fileno())

        # Remove data that is behind the new cursor in case the file has
        # gotten shorter
        self._handle.truncate()