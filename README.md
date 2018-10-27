# sdat2img
Convert sparse Android data image (.dat) into filesystem ext4 image (.img)



## Requirements
This binary requires Python 2.7 or newer installed on your system. 
It currently supports Windows, Linux, MacOS & ARM architectures.

**Note:** newer Google's [Brotli](https://github.com/google/brotli) format (`system.new.dat.br`) must be decompressed to a valid sparse data image before using `sdat2img` binary.



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



## Info
For more information about this binary, visit http://forum.xda-developers.com/android/software-hacking/how-to-conver-lollipop-dat-files-to-t2978952.
