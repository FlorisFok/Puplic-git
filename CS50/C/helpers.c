/************************************************************************
 * Helper functions
 * Floris Fok
 *
 * Sort  linear and bianry and search functions.
 *
 * Binary search is both standard and with recursion,
 * The simple version is commented out.
 * Counting sort and linear or insertion sort are also defined.
 * **********************************************************************/
#define _XOPEN_SOURCE
#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "helpers.h"

#define LIMIT 65536

//struct
struct pos
{
    int max;
    int min;
    int* values;
    int value;
};
// Recursion function
bool find(struct pos set);

// TESTING purpose only
void test(int *array, int n);

// TESTING purpose only //////////////////////
// int main (int c, char* arg[])            //
// {                                        //
//     int n = atoi(arg[1]);                //
//     int array[n];                        //
//     for (int i = 0; i<n; i++)            //
//     {                                    //
//         srand48((long int) i);           //
//         array[i] = drand48()*10000;      //
//     }                                    //
//     int item = array[30];                //
//     sort(array,n);                       //
//     int found = search(item,array,n);    //
//     if (found == 1)                      //
//     {                                    //
//         printf("Found\n");               //
//     }                                    //
// }                                        //
//////////////////////////////////////////////


/////////////////// Normal, first try ////////////////////////////////////////
// Returns true if value is in array of n values, else false
// bool search(int value, int values[], int n)
// {
//     // TODO: implement a searching algorithm (sorted array)
//     if (n < 0)
//     {
//         return false;
//     }

//     int max = n;
//     int min = 0;
//     int max_temp;
//     int min_temp;

//     while (true)
//     {
//         if (value > values[((max-min) / 2) + min])
//         {
//             min_temp = (int) ((max-min) / 2) + min;
//             max_temp = max;
//         }
//         else
//         {
//             max_temp = (int) ((max-min) / 2) + min;
//             min_temp = min;
//         }

//         if (value == values[min_temp] || value ==values[max_temp])
//         {
//             return true;
//         }

//         else if (min == min_temp && max == max_temp)
//         {
//             return false;
//         }
//         max = max_temp;
//         min = min_temp;
//     }
// }

///////////////////  Fancy   search   ////////////////////////////////////////
// Returns true if value is in array of n values, else false
bool search(int value, int values[], int n)
{
    // checks if array is larger then 0 and value is in range of array.
    if (n < 0 || value > values[n - 1] || value < values[0])
    {
        return false;
    }
    //Set struct
    struct pos set;
    set.values = values;
    set.value = value;
    set.max = n;
    set.min = 0;
    return find(set);
}

bool find(struct pos set)
{
    // Checks which side to look
    if (set.value > set.values[((set.max - set.min) / 2) +  set.min])
    {
        set.min = (int) ((set.max - set.min) / 2) + set.min;
    }
    else
    {
        set.max = (int) ((set.max - set.min) / 2) + set.min;
    }
    // checks if value is there or will never be there
    if (set.value == set.values[set.min] ||set.value == set.values[set.max])
    {
        return true;
    }
    else if (set.min == set.max || abs(set.min - set.max) == 1)
    {
        return false;
    }
    // Recursion, until true or false.
    return find(set);
}


//An O(n) sorting algorithm, which sorts an array of n, if n<0 it will not sort.
void sort(int values[], int n)
{
    if (n < 0 || n > LIMIT)
    {
        return;
    }

    // Make array of zero's and count the values.
    // Not sure if limit, or local limit must be used.
    int count_array[LIMIT] = {0};
    for (int i = 0; i < n; i++)
    {
        count_array[values[i]]++;
    }

    // Copy array
    int *copy_array;
    copy_array = &values[0];

    // Place values in right order
    int place = 0;
    for (int i = 0; i < LIMIT; i++)
    {
        //If value is occuring multiple times, it loops and adds it to the array
        //If occures ones, it adds it to the array
        //Ifnot occuring, it skips
        for (int j = 0; j < count_array[i]; j++)
        {
            values[place] = i;
            place++;
        }
    }
    return;
}

///// This is the wrong algorithem, but it works, so i just kept it.///////
// Due to this comment --> TODO: implement an O(n^2) sorting algorithm
// // Sorts array of n values
// No comments, it's selection sort, but not optimized because it was
// the wrong method.
// void sort(int values[], int n)
// {
//
//     if (n < 0 || n > LIMIT)
//     {
//         return;
//     }
//     int sorted[n];
//     for (int i = 0; i<n; i++)
//     {
//         sorted[i] = values[i];
//     }
//     int temp;
//     int sort = 0;
//     while (sort<n)
//     {
//         temp = sorted[sort];
//         int  positions;
//         for (int i = 0; i<n; i++)
//         {
//             if (temp > sorted[i])
//             {
//                 temp = sorted[i];
//                  positions = i;
//             }
//         }
//         values[sort] = temp;
//         sorted[ positions] = LIMIT;
//         sort++;
//     }
//     values = sorted;
//     return;
// }

// TESTING pur positionse only
void test(int *array, int n)
{
    for (int exam = 0; exam<n; exam++)
    {
        printf("%i\n",array[exam]);
    }
}