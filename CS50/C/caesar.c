/******************************************************************************
 * Floris Fok
 * CS50 caesar.c -- student version
 *
 * A program, caesar, that encrypts messages using Caesar’s cipher.
 * ****************************************************************************/
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int char_to_num(char *);
bool is_up(char symbol);
bool is_down(char symbol);
void print_new(char a, char old, int key);

// set boundaries alfabet
char LOW_A = 'a';
char UP_A = 'A';

int main(int arg_count, string cmd[])
{
    //Show correct format of input
    if (arg_count != 2)
    {
        printf("Usage: ./caesar k\n");
        return 1;
    }

    //Request input message
    string input = get_string("plaintext: ");
    printf("ciphertext: ");

    //Convert string to int, so we can use the key
    int key = char_to_num(cmd[1]);

    //Loop all letters and preforms the cipher,
    //skips non letters and perserve uppercases.
    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (is_up(input[i]))
        {
            print_new(UP_A, input[i], key);
        }
        else if (is_down(input[i]))
        {
            print_new(LOW_A, input[i], key);
        }
        else
        {
            printf("%c", input[i]);
        }
    }

    printf("\n");
    return 0;
}

//Own version of atoi(), just for fun.
//Converts to int, subtracts excess numbers to go to normal 0-9 int.
// Adds neccecary zero's to end and adds the numbers.
int char_to_num(char *key)
{
    int key_num = 0;
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        int beta_num = key[i];
        int p = pow(10, (n - i)) / 10;
        int num = (beta_num - '0') * p;
        key_num += num;
    }
    return key_num;
}

//Two funcitons that check if the char is a letter, either upper or lower.
bool is_up(char symbol)
{
    //Checks if symnbol is a uppercase letter
    return 'A' <= symbol && symbol <= 'Z';
}

bool is_down(char symbol)
{
    //Checks if symnbol is a uppercase letter
    return 'a' <= symbol && symbol <= 'z';
}

//Functions that prints the end results, upper or lower depends on the input 'a'
void print_new(char a_char, char old, int key)
{
    // using a 'a' will give lower, 'A' will give upper case
    int ascii = old - a_char;

    // loops only the 26 alfabet, not the whole ascii
    int new_ascii = (key + ascii) % 26;
    printf("%c", a_char + new_ascii);
}