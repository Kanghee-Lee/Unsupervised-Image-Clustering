from PIL import Image
import imagehash_class as imagehash

isFirst = True

# 편의를위해 이미지 이름 내맘대로 수정
gloCount = 0


def make_imghash(userpath, hashfunc=imagehash.average_hash):
    import os
    global gloCount

    def is_image(filename):
        f = filename.lower()

        return f.endswith(".png") or f.endswith(".jpg") or \
               f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif") or '.jpg' in f

    temp_image_filenames = []
    temp_image_filenames += [os.path.join(userpath, path) for path in os.listdir(userpath) if is_image(path)]
    temp_image_filenames = sorted(temp_image_filenames)
    print(temp_image_filenames)
    filename_hash = {}
    image_filenames = []
    for img in temp_image_filenames:
        newName = os.path.dirname(img) + '\\' + str(gloCount) + '_test2.jpg'

        os.rename(img, newName)
        img = newName

        image_filenames.append(img)
        gloCount += 1
        try:
            hash = hashfunc(Image.open(img))
        except Exception as e:
            print('Problem:', e, 'with', img)

        print(img, hash)
        filename_hash[img] = hash
    return filename_hash, image_filenames


def cal_sim(filename_hash, image_filenames):

    for idx1 in range(len(image_filenames)):
        for idx2 in range(idx1 + 1, len(image_filenames)):
            print(image_filenames[idx1][-12:-10], image_filenames[idx2][-12:-10])
            print(filename_hash[image_filenames[idx1]] - filename_hash[image_filenames[idx2]])


if __name__ == '__main__':
    import sys, os

    # hashmethod = sys.argv[1] if len(sys.argv) > 1 else usage()
    hashmethod = 'ahash'
    if hashmethod == 'ahash':
        hashfunc = imagehash.average_hash
    elif hashmethod == 'phash':
        hashfunc = imagehash.phash
    elif hashmethod == 'dhash':
        hashfunc = imagehash.dhash
    elif hashmethod == 'dhash_vertical':
        hashfunc = imagehash.dhash_vertical
    elif hashmethod == 'whash-haar':
        hashfunc = imagehash.whash
    elif hashmethod == 'whash-db4':
        hashfunc = lambda img: imagehash.whash(img, mode='db4')

    userpath = os.getcwd() + '\img3'

    filename_hash, image_filenames = make_imghash(userpath=userpath, hashfunc=hashfunc)
    cal_sim(filename_hash, image_filenames)