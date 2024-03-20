from LZW_image import LZW
import os

compressor = LZW(os.path.join("Images", "image_1.png"))
compressor.compress()

# decompressor = LZW(os.path.join("CompressedFiles", "image_1Compressed.lzw"))
# decompressor.decompress()
