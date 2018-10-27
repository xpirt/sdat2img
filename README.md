# sdat2img
Convert sparse Android data image (.dat) into filesystem ext4 image (.img)



## Requirements
This binary requires Python 2.7 or newer installed on your system.

It currently supports Windows, Linux, MacOS & ARM architectures.



## Usage
```
sdat2img.py <transfer_list> <system_new_file> [system_img]
```
- `<transfer_list>` = input, system.transfer.list from rom zip
- `<system_new_file>` = input, system.new.dat from rom zip
- `[system_img]` = output ext4 raw image file (optional)



## Example
This is a simple example on a Linux system: 
```
~$ ./sdat2img.py system.transfer.list system.new.dat system.img
```



## OTAs
If you are looking on decompressing `system.patch.dat` file or `.p` files, therefore reproduce the patching system on your PC, check [imgpatchtools](https://github.com/erfanoabdi/imgpatchtools) out by @erfanoabdi.


## Brotli compressed data images

If data image is compressed using [brotli](https://github.com/google/brotli/), decompress the data image (`system.new.dat.br`) and then use the script. Windows users can find brotli binaries [here](https://github.com/google/brotli/releases/tag/v1.0.4). If the image is not converted, mounting the generated system.img will result in error similar to this.

```console
~$ sudo mount system.img /mnt/lineage
mount: wrong fs type, bad option, bad superblock on /dev/loop0,
       missing codepage or helper program, or other error
       In some cases useful info is found in syslog - try
       dmesg | tail  or so
```


## Info
For more information about this binary, visit http://forum.xda-developers.com/android/software-hacking/how-to-conver-lollipop-dat-files-to-t2978952.
