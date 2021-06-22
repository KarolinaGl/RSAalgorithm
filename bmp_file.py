from skimage.io import imread, imshow

from constants import *

import matplotlib.pyplot as plt

from utilities import int_to_bytes


def binary_little_endian_to_int(array):
    byte_sum = 0
    multiplier = 1
    for byte in array:
        byte_sum += byte * multiplier
        multiplier *= 2**8
    return byte_sum


class BmpFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.array = self.open_file()

    def get_dib_header_size(self):
        array = BmpFile.open_file(self)
        dib_header_offset = BITMAPV5HEADER['size of DIB header'][0]
        dib_header_field_size = BITMAPV5HEADER['size of DIB header'][1]
        return binary_little_endian_to_int(array[dib_header_offset:(dib_header_offset + dib_header_field_size)])

    def print_file_attributes(self):
        array = BmpFile.open_file(self)

        for key, value in DIB_HEADERS_TO_ATTRIBUTES[self.get_dib_header_size()].items():
            offset, size, function = value
            if offset + size - BITMAPFILEHEADER_SIZE > self.get_dib_header_size():
                continue
            attribute_value = function(array[offset:(offset + size)])
            if key == 'compression method':
                for compression_key in COMPRESSION_METHODS:
                    if attribute_value == compression_key:
                        print(f"{key} = {COMPRESSION_METHODS[compression_key]}")
            elif key == 'halftoning algorithm':
                for halftoning_key in HALFTONING_ALGORITHMS:
                    if attribute_value == halftoning_key:
                        print(f"{key} = {HALFTONING_ALGORITHMS[halftoning_key]}")
            elif key == 'size of DIB header':
                for DIB_key in DIB_HEADERS:
                    if attribute_value == DIB_key:
                        print(f"{key} = {attribute_value} => {DIB_HEADERS[DIB_key]}")
            else:
                print(f"{key} = {attribute_value}")

    def save_encrypted_file(self, split_method):
        encrypted_data = split_method.encrypt(self.get_image_data())
        self._set_new_bitmap_data_size(len(encrypted_data))
        image_header = self.get_image_header()
        image_footer = self.get_image_footer()
        with open("encrypted_file.bmp", "wb") as file:
            file.write(image_header + encrypted_data + image_footer)

    def save_decrypted_file(self, split_method):
        decrypted_data = split_method.decrypt(self.get_image_data())
        self._set_new_bitmap_data_size(len(decrypted_data))
        image_header = self.get_image_header()
        image_footer = self.get_image_footer()
        with open("decrypted_file.bmp", "wb") as file:
            file.write(image_header + decrypted_data + image_footer)

    def open_file(self):
        with open(self.file_name, "rb") as image:
            f = image.read()
            b = bytearray(f)
        return b

    def show(self):
        image = imread(self.file_name)
        plt.imshow(image)
        plt.show()

    def get_image_data(self):
        start, end = self._get_image_data_start_end()
        return self.array[start:end]

    def get_image_header(self):
        start, end = self._get_image_data_start_end()
        return self.array[0:start]

    def get_image_footer(self):
        start, end = self._get_image_data_start_end()
        return self.array[end:len(self.array)]

    def _get_image_data_start_end(self):
        file_attributes = {
            'offset': (10, 4, binary_little_endian_to_int),
            'size of the raw bitmap data': (34, 4, binary_little_endian_to_int),
        }

        def get_value(name):
            offset, size, function = file_attributes[name]
            return function(self.array[offset:(offset + size)])

        offset_value = get_value('offset')
        size_value = get_value('size of the raw bitmap data')

        return offset_value, offset_value + size_value

    def _set_new_bitmap_data_size(self, new_data_size):
        new_data_size_bytes = int_to_bytes(new_data_size)

        tmp = 0
        for i in range(34, 38):
            if tmp < len(new_data_size_bytes):
                self.array[i] = new_data_size_bytes[tmp]
            else:
                self.array[i] = 0
            tmp += 1

