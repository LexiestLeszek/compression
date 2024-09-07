import os

def compress_data(data):
    dictionary = {}
    compressed = bytearray()
    next_code = 256
    buffer = bytearray()

    for byte in data:
        buffer.append(byte)
        if bytes(buffer) not in dictionary:
            if len(buffer) > 1:
                compressed.extend(dictionary[bytes(buffer[:-1])])
            compressed.append(byte)
            dictionary[bytes(buffer)] = next_code.to_bytes(2, byteorder='big')
            next_code += 1
            buffer.clear()
            buffer.append(byte)

    if buffer:
        if len(buffer) > 1:
            compressed.extend(dictionary[bytes(buffer)])
        else:
            compressed.extend(buffer)

    rle_compressed = bytearray()
    count = 1
    prev = compressed[0]

    for byte in compressed[1:]:
        if byte == prev and count < 255:
            count += 1
        else:
            rle_compressed.extend([count, prev])
            count = 1
            prev = byte

    rle_compressed.extend([count, prev])

    return bytes(rle_compressed)

def compress_file(input_file, output_file=None):
    if output_file is None:
        output_file = input_file + '.compressed'

    with open(input_file, 'rb') as f_in:
        data = f_in.read()

    compressed = compress_data(data)

    with open(output_file, 'wb') as f_out:
        f_out.write(compressed)

    print(f"Original size: {len(data)} bytes")
    print(f"Compressed size: {len(compressed)} bytes")
    print(f"Compression ratio: {len(compressed) / len(data):.2f}")

    return output_file

def decompress_data(compressed_data):
    rle_decompressed = bytearray()
    for i in range(0, len(compressed_data), 2):
        count = compressed_data[i]
        byte = compressed_data[i + 1]
        rle_decompressed.extend([byte] * count)

    dictionary = {i.to_bytes(2, byteorder='big'): bytes([i]) for i in range(256)}
    next_code = 256
    decompressed = bytearray()
    buffer = bytearray()

    for byte in rle_decompressed:
        buffer.append(byte)
        if bytes(buffer) in dictionary:
            decompressed.extend(dictionary[bytes(buffer)])
            if len(buffer) > 1:
                new_entry = dictionary[bytes(buffer[:-1])] + bytes([byte])
                dictionary[next_code.to_bytes(2, byteorder='big')] = new_entry
                next_code += 1
            buffer.clear()

    return bytes(decompressed)

def decompress_file(input_file, output_file=None):
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.decompressed'

    with open(input_file, 'rb') as f_in:
        compressed_data = f_in.read()

    decompressed = decompress_data(compressed_data)

    with open(output_file, 'wb') as f_out:
        f_out.write(decompressed)

    print(f"Decompressed size: {len(decompressed)} bytes")

    return output_file

if __name__ == "main":
    input_file = "example.txt"

    compressed_file = compress_file(input_file)
    print(f"File compressed: {compressed_file}")

    decompressed_file = decompress_file(compressed_file)
    print(f"File decompressed: {decompressed_file}")

    with open(input_file, 'rb') as f1, open(decompressed_file, 'rb') as f2:
        if f1.read() == f2.read():
            print("Decompression successful: files are identical")
        else:
            print("Decompression failed: files are different")
