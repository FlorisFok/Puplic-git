// This code checks if the credit card number of three major companies is valid
#include <stdio.h>
#include <cs50.h>

long long int input;
int total = 0;
int num_one;
int num_two;
int digit;
int first;
int second;

int check_dubbel(int n);
bool check_company(int num, int num2, int length);

int main(void)
{
    //Ask input, till correct format is applied, a positive interger (long long)
    do
    {
        input = get_long_long("Number: ");
    }
    while (input < 0);

    int even = 0;
    //Itterate though numbers by using the rest of dividing by 10 and then divide by 10 to get the next number,
    // switching action on even and uneven numbers
    while (input != 0)
    {
        digit = (input % 10);
        input /= 10;
        if (even % 2 == 0)
        {
            //Even numbers are added
            total += digit;
            num_one = digit;
        }
        else
        {
            //Odd numbers are multiplied by 2 and added, but if: it has two digits after multiplycation,
            // the two digits are summed and added.
            total += check_dubbel(digit * 2);
            num_two = digit;
        }
        even++;
    }

    //Last two digits saved are the first two digits, the order is corrected here.
    if (even % 2 == 0)
    {
        first = num_two;
        second = num_one;
    }
    else
    {
        first = num_one;
        second = num_two;
    }

    //Check if the formula ends on 0, thus is VALID and if it fits a company profile; ifnot returns INVALLID
    if (total % 10 == 0)
    {
        if (check_company(first, second, even))
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

//Funtion for checking the dubbel digit numbers, if dubbel; adding one to the last digit, since none is exceeding 18.
// if not dubble, simply returns the value
int check_dubbel(int n)
{
    if ((n / 10) != 0)
    {
        return ((n % 10) + 1);
    }
    else
    {
        return n;
    }
}

// Fucntion for all the company matches, Few charactaristics are checked to see if it fits one of the profiles.
// Prints if it finds a name, returns true if not.
bool check_company(int num, int num2, int length)
{
    //Returns true, if it is not found
    bool not_found = true;
    //Check if it's a VISA
    if (num == 4)
    {
        if (length == 13 || length == 16)
        {
            printf("VISA\n");
            not_found = false;
        }
    }
    //Check if it's a America Express
    else if (num == 3 && length == 15)
    {
        if (num2 == 4 || num2 == 7)
        {
            printf("AMEX\n");
            not_found = false;
        }
    }
    //Check if it's a MasterCard
    else if (num == 5 && length == 16)
    {
        if (num2 == 1 || num2 == 2 || num2 == 3 || num2 == 4 || num2 == 5)
        {
            printf("MASTERCARD\n");
            not_found = false;
        }
    }
    return not_found;
}