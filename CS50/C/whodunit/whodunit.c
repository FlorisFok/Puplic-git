/************************************************************************
 * Computer version of WHODUNIT secret message decoder.
 * Floris Fok
 *
 * Find off color bytes in a (almost) all red picture.
 * makes the picture readable
 * **********************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

#include "bmp.h"

unsigned int MAX_VALUE = 255;

int main(int argc, char *argv[])
{
    // ensure proper format
    if (argc != 3)
    {
        fprintf(stderr, "Usage: ./whodunit infile outfile\n");
        return 1;
    }

    // extract file names
    char *in_file = argv[1];
    char *out_file = argv[2];

    // open input file
    FILE *input = fopen(in_file, "r");
    if (input == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", in_file);
        return 2;
    }

    // open output file
    FILE *write_file = fopen(out_file, "w");
    if (write_file == NULL)
    {
        fclose(write_file);
        fprintf(stderr, "Could not create %s.\n", out_file);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, input);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, input);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(write_file);
        fclose(input);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, write_file);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, write_file);

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, input);

            //If it is not fully red, make pixel black
            if (triple.rgbtRed != MAX_VALUE)
            {
                triple.rgbtRed = 0;
                triple.rgbtBlue = 0;
                triple.rgbtGreen = 0;
            }
            //Else make it white, thus more readable
            else
            {
                triple.rgbtRed = MAX_VALUE;
                triple.rgbtBlue = MAX_VALUE;
                triple.rgbtGreen = MAX_VALUE;
            }
            // write RGB triple to outfile
            fwrite(&triple, sizeof(RGBTRIPLE), 1, write_file);
        }
        // skip over padding, if any
        fseek(input, padding, SEEK_CUR);

        // then add it back (to demonstrate how)
        for (int k = 0; k < padding; k++)
        {
            fputc(0x00, write_file);
        }
    }

    // close infile
    fclose(input);

    // close outfile
    fclose(write_file);

    // success
    return 0;
}