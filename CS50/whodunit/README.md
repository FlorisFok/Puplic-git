# Questions

## What's `stdint.h`?

A header file which declares a set of integer types having specified widths.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

Smaller data types such as uint8_t save space. unint is a unsigned and can only store positives, but therefore can store twice as many positives.
So if you know you only expect positives, you can save space by using unsigned. for example, 32 int holds
2,147,483,647 as maximum and uint 32 4,294,967,295.

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

BYTE = 1;
DWORD = 4;
LONG = 4;
WORD = 2;

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be?
## Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

"BM"

## What's the difference between `bfSize` and `biSize`?

biSize: Number of bytes in the DIB header
bfSize: Size of the BMP file in bytes

## What does it mean if `biHeight` is negative?

Nothing, just use the ABS()

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

WORD biBitCount;

## Why might `fopen` return `NULL` in lines 24 and 32 of `copy.c`?

If the file doesn't exist or that there is no space to create the file (allocation problem)

## Why is the third argument to `fread` always `1` in our code?

We define the size to be a big as the part we need, so when we declare size to be bitheader,
the third argument must be one to read only the bitheader, same with the rgbs. The third
argument is multiplied with the second to determin the read size.

## What value does line 63 of `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

It looks at the end of the line if there is any padding, by seeking values at current
location + padding.

## What is `SEEK_CUR`?

Equal to the current position of the pointer.
