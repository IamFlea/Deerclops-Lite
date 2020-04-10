import time

class Reader(object):
    # Checks if the file was reseted
    UPDATE_CHECK = 60

    def __init__(self, filename):
        super(Reader, self).__init__()
        self.filename = filename
        # File handler
        self.fh = open(filename, 'rb') 
        # Skip the saved stuff in the file
        self.file_idx = len(self.fh.read()) # For `logCleared` method
        self.read_count = 0
        

    # Close the file
    def __del__(self):
        try:
            self.fh.close()
        except:
            print(f"Failed to close: {self.filename}")

    """
    When server is restarted, its logs are cleared. 
    This function checks if the server was restarted
    @return bool
    """
    def logCleared(self):
        # Look if we can select a char before the last char
        idx = self.file_idx - 20 if self.file_idx - 20 > 0 else 0

        if idx < 0:
            return False
        try:
            with open(self.filename, 'rb') as fh:
                fh.read()[idx]
        except IndexError:
            return True
        except MemoryError:
            print(f"MemoryError; retrying in the three seconds")
            time.sleep(3) 
            return True
        except (FileNotFoundError, ValueError):  # Empty file or closed
            return False
        return False
    
    def read(self):
        # Increment and make sure it is in a ring of `UPDATE_CHECK`
        self.read_count = (self.read_count + 1) % Reader.UPDATE_CHECK
        # Reload handler if necessary
        if self.read_count == 0 and self.logCleared():
            self.file_idx = 0
            try:
                self.fh.close() 
            except:
                pass
            try: 
                self.fh = open(self.filename, 'rb')
            except FileNotFoundError:
                self.read_count = Reader.UPDATE_CHECK - 1
                return ""
        try:
            log = self.fh.read()
        except ValueError:
            log = ""
        self.file_idx += len(log)
        try:
            return log.decode("utf-8")
        except UnicodeDecodeError:
            print(f'Encoding error, skipping. Index: {self.file_idx}')
            return ''
    
    def empty(self):
        return self.file_idx == 0
