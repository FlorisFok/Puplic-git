/******************************************************************************
 * Floris Fok
 * CS50 initials.c -- student version
 *
 * Gives initials of a full name, gotten from command line input.
 * ****************************************************************************/
#include <stdio.h>
#include <cs50.h>

bool is_letter(char symbol);
char to_up(char letter);

int main(void)
{
    //Get input from user
    string s = get_string();

    //counter variable and possible first letter bool
    int i = 0;
    bool first = true;

    while (s[i] != '\0')
    {
        // convert to uppercase, check if it's a letter and if its after a space
        // and prints the uppercase letter.
        char high_letter = to_up(s[i]);
        int letter_bool = is_letter(high_letter);
        if (first == true && letter_bool == 1)
        {
            printf("%c", high_letter);
            first = false;
        }
        // converts first to true, if a space or non letter is detected.
        // in this way the program know next step, incase it's a letter
        // is needed to be printed out.
        else if (letter_bool == 0)
        {
            first = true;
        }
        i++;
    }
    // Prints new line.
    printf("\n");
    return 0;
}


// Function to convert lower to upper and ignore upper letters
char to_up(char letter)
{
    // Checks if it's lowercase, ifyes: make uppercase, ifnot: return value
    if ('a' <= letter && letter <= 'z')
    {
        letter -=  'a' - 'A';
        return letter;
    }
    else
    {
        return letter;
    }
}

// Functions that returns a true or 1 if it is given a letter
bool is_letter(char symbol)
{
    //Checks if symnbol is a uppercase letter
    return 'A' <= symbol && symbol <= 'Z';
}