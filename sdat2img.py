#!/usr/bin/env python
import argparse
import os

BLOCK_SIZE = 4096


def range_set(src):
    src_set = src.split(',')
    num_set = [int(item) for item in src_set]
    if len(num_set) != num_set[0]+1:
        raise ValueError(
            'Error on parsing following data to range_set:\n{}'.format(src))
    return tuple([(num_set[i], num_set[i+1])
                 for i in range(1, len(num_set), 2)])


def transfer_list_file_to_commands(trans_list):
    version = int(trans_list.readline())
    trans_list.readline()  # new blocks
    if version >= 2:
        trans_list.readline()  # simultaneously stashed entries
        trans_list.readline()  # max num blocks simultaneously stashed

    commands = []
    for line in trans_list:
        line = line.split(' ')
        cmd = line[0]
        if cmd in ['erase', 'new', 'zero']:
            commands.append([cmd, range_set(line[1])])
        else:
            if not cmd[0].isdigit():
                raise ValueError('Command "{}" is not valid.'.format(cmd))

    return commands


def main(transfer_list_file, new_dat_file, output_filename):
    commands = transfer_list_file_to_commands(transfer_list_file)

    if os.path.exists(output_filename):
        raise ValueError(
            'Error: the output file "{}" already exists'
            'Remove it, rename it, or choose a different file name.'
            .format(output_filename))

    with open(output_filename, 'wb') as output_img:
        all_block_sets = [i for command in commands for i in command[1]]
        max_file_size = max(pair[1] for pair in all_block_sets) * BLOCK_SIZE

        for command in commands:
            if command[0] == 'new':
                for block in command[1]:
                    begin = block[0]
                    end = block[1]
                    block_count = end - begin
                    print('Copying {} blocks to position {}...'.format(
                        block_count, begin))
                    output_img.seek(begin * BLOCK_SIZE)
                    while block_count > 0:
                        output_img.write(new_dat_file.read(BLOCK_SIZE))
                        block_count -= 1
            else:
                print('Skipping command {}'.format(command[0]))

        # Make file larger if necessary
        if(output_img.tell() < max_file_size):
            output_img.truncate(max_file_size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('transfer_list', help='transfer list file')
    parser.add_argument('new_dat', help='system new dat file')
    parser.add_argument('output', default='output.img',
                        help='output image')
    args = parser.parse_args()
    with open(args.transfer_list, 'r') as transfer_list_file:
        with open(args.new_dat, 'rb') as new_dat_file:
            main(transfer_list_file, new_dat_file, args.output)
