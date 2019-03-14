/************************************************************************
 * Resize bit map image.
 * Floris Fok
 *
 * Takes a file.bmp and a scale, which it rescales to another file.bmp.
 * **********************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper format
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize f infile outfile\n");
        return 1;
    }
    // extract file names and float
    const float resize_value = atof(argv[1]);
    char *in_file = argv[2];
    char *out_file = argv[3];

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

    //Keep old size, and make matrix
    int old_width = bi.biWidth;
    int old_height = abs(bi.biHeight);
    int old_image[old_width][old_height][3];

    //calculate new size
    int new_height = old_height * resize_value;
    int new_width = old_width * resize_value;

    //Changes in BITHEADER
    bi.biWidth = new_width;
    bi.biHeight = -new_height;

    //Calulate paddings
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int old_padding = (4 - (old_width * sizeof(RGBTRIPLE)) % 4) % 4;

    //Change Bitheader continpous
    bi.biSizeImage = 3 * new_width * new_height + new_height * padding;
    bf.bfSize = 54 + bi.biSizeImage;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, write_file);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, write_file);

    // iterate over infile's scanlines
    for (int i = 0; i < old_height; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0; j < old_width; j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, input);
            //Save image in matrix
            old_image[i][j][0] = triple.rgbtRed;
            old_image[i][j][1] = triple.rgbtGreen;
            old_image[i][j][2] = triple.rgbtBlue;

        }

        // skip over padding, if any
        fseek(input, old_padding, SEEK_CUR);
    }

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
    {
        //Determine pixel mapping value x axis
        int i2 = (int) i / resize_value;
        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;
            //Determine pixel mapping value y axis
            int j2 = (int) j / resize_value;

            //Map pixel to temporary RGB
            triple.rgbtRed = old_image[i2][j2][0];
            triple.rgbtGreen = old_image[i2][j2][1];
            triple.rgbtBlue = old_image[i2][j2][2];

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