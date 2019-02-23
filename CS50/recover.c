/************************************************************************
 * Recovering of jpg files
 * Floris Fok
 *
 * recovers jpg pictures from a continous array of bytes, finds starting
 * bytes and everyting in between will be exported as a numberd image file.
 * till file is empty.
 * **********************************************************************/
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>
#include <stdint.h>

// Global vars
typedef uint8_t  BYTE;
const int FILE_NAME_LEN  = 3;
const int BLOCK_SIZE = 512;

// Functions
bool is_jpg(BYTE *bytes);
string name_file(int i);

int main(int argc, char *argv[])
{
    // Ensure proper format
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }
    // Open file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    BYTE temp_bytes[BLOCK_SIZE];
    int file_num = 0;
    bool open = false;
    FILE *write_file;

    // As long there are parts to read, it will continue
    while (fread(&temp_bytes, 1, BLOCK_SIZE, file))
    {
        // Seraches for the start of a jpg.
        if (is_jpg(temp_bytes))
        {
            // if there is a file open, close it.
            if (open)
            {
                fclose(write_file);
            }

            // create file and unique name.
            string out_file = name_file(file_num);
            write_file = fopen(out_file, "w");
            if (write_file == NULL)
            {
                fclose(write_file);
                fprintf(stderr, "Could not create %s.\n", out_file);
                return 3;
            }
            // free allocated memory of the name.
            // Write the byte block in the file.
            free(out_file);
            fwrite(&temp_bytes, 1, BLOCK_SIZE, write_file);

            // Conclude there is a file in use, and plus one the file number.
            file_num++;
            open = true;
        }
        // If a file is open, keep writing (till next jpg is found)
        else if (open)
        {
            fwrite(&temp_bytes, 1, BLOCK_SIZE, write_file);
        }
    }
    // CLose last file
    fclose(write_file);

    return 0;
}


// Composes a name for the file, numbers from 000 to 999 when FILE_NAME_LEN = 3
string name_file(int i)
{
    //Allocs mem, so it can be transferred to __main__
    char *num_name = (char *) malloc(FILE_NAME_LEN + 4);
    num_name[FILE_NAME_LEN] = '.';
    num_name[FILE_NAME_LEN + 1] = 'j';
    num_name[FILE_NAME_LEN + 2] = 'p';
    num_name[FILE_NAME_LEN + 3] = 'g';
    //For every possibility, 0 or the given number, example: 001 or 392
    for (int n = 1; n <= FILE_NAME_LEN; n++)
    {
        int num = i % 10;
        int place = FILE_NAME_LEN - n;
        num_name[place] = (char) num + '0';
        i /= 10;

    }
    return (string) num_name;
}

// Checks if first bytes are equal to jpg.
bool is_jpg(BYTE *bytes)
{
    return (bytes[0] == 0xff &&
            bytes[1] == 0xd8 &&
            bytes[2] == 0xff &&
            (bytes[3] & 0xf0) == 0xe0);
}