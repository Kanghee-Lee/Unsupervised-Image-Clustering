from PIL import Image
import numpy


def _binary_array_to_hex(arr):
    """
    bool type array -> binary string -> hex string으로 변환 ex) [True False True True] -> 1011 -> e
    """
    bit_string = ''.join(str(b) for b in 1 * arr.flatten())
    width = int(numpy.ceil(len(bit_string) / 4))  # 16진수로 바꿀때 길이지정
    return '{:0>{width}x}'.format(int(bit_string, 2), width=width)


class ImageHash(object):
    def __init__(self, binary_array):
        self.hash = binary_array
        self.group_number = -1  # Todo : mlkit랑 다시 작업 group에 대해서

    def group_number(self):
        return self.group_number

    def __str__(self):
        return _binary_array_to_hex(self.hash.flatten())

    def __repr__(self):
        return repr(self.hash)

    def __sub__(self, other):
        if other is None:
            raise TypeError('Other hash must not be None.')
        if self.hash.size != other.hash.size:
            raise TypeError('ImageHashes must be same shape.', self.hash.shape, other.hash.shape)
        return numpy.count_nonzero(self.hash.flatten() != other.hash.flatten())

    def __eq__(self, other):
        if other is None:
            return False
        return numpy.array_equal(self.hash.flatten(), other.hash.flatten())

    def __ne__(self, other):
        if other is None:
            return False
        return not numpy.array_equal(self.hash.flatten(), other.hash.flatten())

    def __hash__(self):
        # 딕셔너리에서 빠른 키 비교를 위해 8bit 정수 return
        return sum([2 ** (i % 8) for i, v in enumerate(self.hash.flatten()) if v])


'''
일단은 필요 없어보임
def hex_to_hash(hexstr):
    hash_size = int(numpy.sqrt(len(hexstr) * 4))
    binary_array = '{:0>{width}b}'.format(int(hexstr, 16), width=hash_size * hash_size)

    bit_rows = [binary_array[i:i + hash_size] for i in range(0, len(binary_array), hash_size)]
    hash_array = numpy.array([[bool(int(d)) for d in row] for row in bit_rows])
    return ImageHash(hash_array)
'''


def average_hash(image, hash_size=8):
    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")

    # ANTIALIAS를 이용한 보간법으로 크기 줄임 & grayscale
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    # numpy.asarray로 image의 참조형태 배열 생성 -> image변경되면 배열도 같이 바껴야하니까
    pixels = numpy.asarray(image)
    avg = pixels.mean()

    diff = pixels > avg

    return ImageHash(diff)


'''
지금으로썬 ahash로 쭉 갈 가능성 높음
def phash(image, hash_size=8, highfreq_factor=4):

    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")

    import scipy.fftpack
    img_size = hash_size * highfreq_factor
    image = image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = numpy.asarray(image)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = numpy.median(dctlowfreq)
    diff = dctlowfreq > med
    return ImageHash(diff)


def phash_simple(image, hash_size=8, highfreq_factor=4):
    import scipy.fftpack
    img_size = hash_size * highfreq_factor
    image = image.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
    pixels = numpy.asarray(image)
    dct = scipy.fftpack.dct(pixels)
    dctlowfreq = dct[:hash_size, 1:hash_size + 1]
    avg = dctlowfreq.mean()
    diff = dctlowfreq > avg
    return ImageHash(diff)


def dhash(image, hash_size=8):
    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")

    image = image.convert("L").resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    pixels = numpy.asarray(image)
    # compute differences between columns
    diff = pixels[:, 1:] > pixels[:, :-1]
    return ImageHash(diff)


def dhash_vertical(image, hash_size=8):
    image = image.convert("L").resize((hash_size, hash_size + 1), Image.ANTIALIAS)
    pixels = numpy.asarray(image)
    diff = pixels[1:, :] > pixels[:-1, :]
    return ImageHash(diff)


def whash(image, hash_size=8, image_scale=None, mode='haar', remove_max_haar_ll=True):
    import pywt
    if image_scale is not None:
        assert image_scale & (image_scale - 1) == 0, "image_scale is not power of 2"
    else:
        image_natural_scale = 2 ** int(numpy.log2(min(image.size)))
        image_scale = max(image_natural_scale, hash_size)

    ll_max_level = int(numpy.log2(image_scale))

    level = int(numpy.log2(hash_size))
    assert hash_size & (hash_size - 1) == 0, "hash_size is not power of 2"
    assert level <= ll_max_level, "hash_size in a wrong range"
    dwt_level = ll_max_level - level

    image = image.convert("L").resize((image_scale, image_scale), Image.ANTIALIAS)
    pixels = numpy.asarray(image) / 255

    if remove_max_haar_ll:
        coeffs = pywt.wavedec2(pixels, 'haar', level=ll_max_level)
        coeffs = list(coeffs)
        coeffs[0] *= 0
        pixels = pywt.waverec2(coeffs, 'haar')

    coeffs = pywt.wavedec2(pixels, mode, level=dwt_level)
    dwt_low = coeffs[0]

    med = numpy.median(dwt_low)
    diff = dwt_low > med
    return ImageHash(diff)
'''