/******************************************************************************
 * Floris Fok
 * CS50 crack.c -- student version
 *
 * A program, Crack, that cracks hash passwords up to a pre-determent length.
 * ****************************************************************************/
#define _XOPEN_SOURCE

#include <unistd.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

// Define max length of passwords, and max symbols
int MAX_LEN = 5;
int MAX_SYM = 52;

char try_char(int i);

int main(int arg_count, string cmd[])
{
    //Only works if a single hash is given and has a length of 13, otherwise
    // retruns format preference
    if (arg_count != 2 && strlen(cmd[1]) == 13)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }

    //Get input hash
    string hash = cmd[1];

    //Get input salt
    char salt[2];
    salt[0] = hash[0];
    salt[1] = hash[1];

    // lenght is used outside the loop
    int length;

    //Start with passwords with length one, untill MAX_LEN is surpassed
    for (length = 1; length <= MAX_LEN; length++)
    {
        //Makes char* that hold places for the password, and size optimized.
        char key[length+1];
        key[length] = '\0';

        //Iterate through all the possibilities for that perticulair length
        for (int i = 0; i < pow(MAX_SYM,length); i++)
        {
            //Iterates through all char places, and assigns a symbol.
            for (int place = 0; place < length; place++)
            {
                //Each i got his own combiantion of symbols, therefor their is
                // only one counting var. Each symbol is calculated by it's
                // position. Every MAX_SYM, the first symbol has done a full
                // Cycle and every max_sym*max_sym, the second.. ect.
                key[place] = try_char(((i / ( (int) pow(MAX_SYM, place)))
                                   % MAX_SYM));
            }
            //Creates new hash and compares it with the old hash, if they match
            // the key is printed, because we broke the hash!
            string hash2 = crypt(key, salt);
            if (strcmp(hash, hash2) == 0)
            {
                printf("%s\n", key);
                //Breaks loop
                length = 999; break;
            }
        }

    }
    //If not found; execute this.
    if (length != 1000)
    {
        printf("\rNOT FOUND");
    }
    return 0;
}
//cycles though all possible symbols or in this case; letters (up and low)
// takes an int as input and returns the corresponding char.
char try_char(int i)
{
    char l = '0';
    if (i < 26)
    {
        l = 'A' + i;
    }
    else if (i >= 26)
    {
        l = 'a' + i % 26;
    }
    return l;
}