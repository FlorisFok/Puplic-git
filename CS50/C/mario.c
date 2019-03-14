//Prints a mario piramide for a certain height, given by user input
#include <cs50.h>
#include <stdio.h>

void print_piramid(int n);
void print_blocks(int b);

int main(void)
{
    int height;
    //Gets user input
    do
    {
        height = get_int("Height: ");
    }
    while (height < 0 || height > 23);
    //Make piramide
    print_piramid(height);
}


void print_piramid(int max_height)
//Creates the piramide for a certain height
//Input: Maximal height of mario piramide
//Output: prints in cmd
{
    //For loop, printing each line
    for (int layer = 0; layer < max_height; layer++)
    {
        int blocks = layer + 1;

        //Print space(s) to print
        for (int i = 0; i < max_height - (blocks); i++)
        {
            printf(" ");
        }
        // Print blocks
        print_blocks(blocks);

        //Print 'GAP'
        printf("  ");

        //Print blocks
        print_blocks(blocks);

        // Go to new line
        printf("\n");
    }
}

void print_blocks(int blocks)
{
    //For every block print one #
    for (int i = 0; i < blocks; i++)
    {
        printf("#");
    }
}