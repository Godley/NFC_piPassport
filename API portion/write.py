import nxppy

mifare = nxppy.Mifare()
uid = mifare.select() # Select the first available tag and return the UID
block10bytes = mifare.read_block(10) # Read 16 bytes starting from block 10 (each block is 4 bytes, so technically this reads blocks 10-13)
mifare.write_block(10, b'abcd') # Write a single block of 4 bytes
print str(block10bytes)
