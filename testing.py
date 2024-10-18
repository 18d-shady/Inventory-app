#import sys # TESTING

#use the winfr tool

def open_physical_drive(
    number,
    mode="rb",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
):
    """
    Opens a physical drive in read binary mode by default
    The numbering starts with 0
    """
    return open(
        fr"\\.\PhysicalDrive{number}",
        mode,
        buffering,
        encoding,
        errors,
        newline,
        closefd,
        opener,
    )

def open_windows_partition(
    letter,
    mode="rb",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
):
    """
    Opens a partition of a windows drive letter in read binary mode by default
    """
    return open(
        fr"\\.\{letter}:", mode, buffering, encoding, errors, newline, closefd, opener
    )


# first 16 bytes from partition C:
# on Linux it's like /dev/sda1
with open_windows_partition("C") as drive_c:
    print(drive_c.read(16))


# first 16 bytes of first drive
# on Linux it's like /dev/sda
with open_physical_drive(0) as drive_0:
    print(drive_0.read(16))
"""
    
drive = "\\\\.\\PhysicalDrive0"     # Open drive as raw bytes
fileD = open(drive, "rb")
size = 512              # Size of bytes to read
byte = fileD.read(size) # Read 'size' bytes
offs = 0                # Offset location
drec = False            # Recovery mode
rcvd = 0                # Recovered file ID
while byte:
    found = byte.find(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a')
    if found >= 0:
        drec = True
        print('==== Found PNG at location: ' + str(hex(found+(size*offs))) + ' ====')
        fileN = open(str(rcvd) + '.png', "wb")
        fileN.write(byte[found:])
        while drec:
            byte = fileD.read(size)
            bfind = byte.find(b'\xae\x42\x60\x82')
            if bfind >= 0:
                fileN.write(byte[:bfind+4])
                fileD.seek((offs+1)*size)
                print('==== Wrote PNG to location: ' + str(rcvd) + '.png ====\n')
                drec = False
                rcvd += 1
                fileN.close()
            else: fileN.write(byte)
        # Now lets create recovered file and search for ending signature
        #sys.exit() # TESTING STOP AFTER FINDING FIRST PNG IMAGE
    byte = fileD.read(size)
    offs += 1
fileD.close()
"""
