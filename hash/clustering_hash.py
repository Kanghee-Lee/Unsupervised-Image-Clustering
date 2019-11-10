from PIL import Image
import hash.imagehash_class as imagehash

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

'''
def cal_sim(filename_hash, image_filenames):

    for idx1 in range(len(image_filenames)):
        for idx2 in range(idx1 + 1, len(image_filenames)):
            print(image_filenames[idx1][-12:-10], image_filenames[idx2][-12:-10])
            print(filename_hash[image_filenames[idx1]] - filename_hash[image_filenames[idx2]])
'''
#grouping
global_count=1
def cal_sim(hash1, hash2):
    return hash1-hash2

same_group=[]
def grouping(filename_hash, image_filenames):
    global global_count
    for idx1 in range(len(image_filenames)):
        for idx2 in range(idx1 + 1, len(image_filenames)):
            hash1, hash2=filename_hash[image_filenames[idx1]], filename_hash[image_filenames[idx2]]
            sim=cal_sim(hash1, hash2)
            sim2=cal_sim(hash2, hash1)
            sim=min(sim, sim2)
            if sim <=55 :
                if hash1.group_number==-1 and hash2.group_number==-1 :
                    hash1.group_number, hash2.group_number=global_count, global_count
                    global_count+=1
                elif hash1.group_number==-1 :
                    hash1.group_number = hash2.group_number
                elif hash2.group_number==-1 :
                    hash2.group_number = hash1.group_number
                elif hash1.group_number!=hash2.group_number:
                    same_group.append([hash1.group_number, hash2.group_number])
            print(image_filenames[idx1][-12:-9], image_filenames[idx2][-12:-9])
            print(sim)

group_dict={}
def print_group(filename_hash, image_filenames) :
    global same_group
    for idx1 in range(len(image_filenames)):
        if filename_hash[image_filenames[idx1]].group_number in group_dict.keys():
            group_dict[filename_hash[image_filenames[idx1]].group_number].append(image_filenames[idx1][-12:-9])
        else :
            group_dict[filename_hash[image_filenames[idx1]].group_number] =[image_filenames[idx1][-12:-9]]
    print(same_group)
    print(group_dict)

#grouping

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

    userpath = os.getcwd() + r'\realtest'
#images3_3 -> 4x4 for문으로 16개씩 hash코드 생성해보자
    filename_hash, image_filenames = make_imghash(userpath=userpath, hashfunc=hashfunc)
    grouping(filename_hash, image_filenames)
    print_group(filename_hash, image_filenames)