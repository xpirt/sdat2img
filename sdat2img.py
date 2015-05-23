#!/usr/bin/env python
#encoding:utf8
#====================================================
#          FILE: sdat2img.py
#       AUTHORS: xpirt - luxi78 - howellzhu - joaormatos
#          DATE: 2015-05-23 19:36:50 UTC
#====================================================
import sys, os, errno

try:
    TRANSFER_LIST_FILE = str(sys.argv[1])
    NEW_DATA_FILE = str(sys.argv[2])
    OUTPUT_IMAGE_FILE = str(sys.argv[3])
except IndexError:
   print ("\nsdat2img - usage is: \n\n      sdat2img <transfer_list> <system_new_file> <system_img>\n\n")
   print ("Visit xda thread for more information.\n")
   try:
       input = raw_input
   except NameError: pass
   input ("Press any key to exit\n")
   sys.exit()

BLOCK_SIZE = 4096

def rangeset(src):
    src_set = src.split(',')
    num_set =  [int(item) for item in src_set]
    if len(num_set) != num_set[0]+1:
        print ('Error on parsing following data to rangeset:\n%s' % src)
        sys.exit(1)

    return tuple ([ (num_set[i], num_set[i+1]) for i in range(1, len(num_set), 2) ])

def parse_transfer_list_file(path):
    trans_list = open(TRANSFER_LIST_FILE, 'r')
    version = int(trans_list.readline())    # 1st line = transfer list version
    new_blocks = int(trans_list.readline()) # 2nd line = total number of blocks

    # version 2 introduced with android-5.1.0_r1
    # skip next 2 lines. we don't need this stuff now
    if version >= 2:
        trans_list.readline()               # 3rd line = stash entries needed simultaneously
        trans_list.readline()               # 4th line = number of blocks that will be stashed

    for line in trans_list:
        line = line.split(' ')              # 5th & next lines should be only commands
        cmd = line[0]
        if 'erase' == cmd:
            erase_block_set = rangeset(line[1])
        elif 'new' == cmd:
            new_block_set = rangeset(line[1])
        else:
            # skip lines starting with numbers, they're not commands anyway.
            if not cmd[0].isdigit():
                print ('No valid command: %s.' % cmd)
                trans_list.close()
                sys.exit(1)

    trans_list.close()
    return version, new_blocks, erase_block_set, new_block_set

def main(argv):
    version, new_blocks, erase_block_set, new_block_set =  parse_transfer_list_file(TRANSFER_LIST_FILE)

    # Don't clobber existing files to avoid accidental data loss.
    try:
        output_img = open(OUTPUT_IMAGE_FILE, 'wxb')
    except IOError as e:
        if e.errno == errno.EEXIST:
            print('Error: the output file "{}" already exists'.format(e.filename))
            print('Remove it, rename it, or choose a different file name.')
            sys.exit(e.errno)
        else:
            raise

    new_data_file = open(NEW_DATA_FILE, 'rb')
    max_file_size = max(pair[1] for pair in erase_block_set)*BLOCK_SIZE

    for block in new_block_set:
        begin = block[0]
        end = block[1]
        block_count = end - begin
        print('Copying {} blocks into position {}...'.format(block_count, begin))

        # Position output file.
        output_img.seek(begin*BLOCK_SIZE)

        # Copy one block at a time.
        while(block_count > 0):
            output_img.write(new_data_file.read(BLOCK_SIZE))
            block_count -= 1

    # Make file larger if necessary
    if(output_img.tell() < max_file_size):
        output_img.truncate(max_file_size)

    output_img.close()
    new_data_file.close()
    print ('\nDone! Output image: %s' % os.path.realpath(output_img.name))

if __name__ == "__main__":
    main(sys.argv)
