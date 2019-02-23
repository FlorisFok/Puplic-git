/************************************************************************
 * The game fifteen
 * Floris Fok
 *
 *
 * playable Game of Fifteen (generalized to d x d)
 * **********************************************************************/

#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

// Constants
#define DIM_MIN 3
#define DIM_MAX 9
#define COLOR "\033[32m"

// Board
int board[DIM_MAX][DIM_MAX];

// Dimensions
int d;

// Saved locations of the blank tile
int blank_row;
int blank_col;

// Prototypes
void clear(void);
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);
void swap(int *a, int *b);
void print_grid_row(int d);
void print_tile(int tile);

int main(int argc, string argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    // Ensure valid dimensions
    d = atoi(argv[1]);
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
               DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    // Open log
    FILE *file = fopen("log.txt", "w");
    if (file == NULL)
    {
        return 3;
    }

    // Greet user with instructions
    greet();

    // Initialize the board
    init();

    // Accept moves until game is won
    while (true)
    {
        // Clear the screen
        clear();

        // Draw the current state of the board
        draw();

        // Log the current state of the board (for testing)
        for (int i = 0; i < d; i++)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        // Check for win
        if (won())
        {
            printf("ftw!\n");
            break;
        }

        // Prompt for move
        printf("Tile to move: ");
        int tile = get_int();

        // Quit if user inputs 0 (for testing)
        if (tile == 0)
        {
            break;
        }

        // Log move (for testing)
        fprintf(file, "%i\n", tile);
        fflush(file);

        // Move if possible, else report illegality
        if (!move(tile))
        {
            printf("\nIllegal move.\n");
            usleep(50000);
        }

        // Sleep thread for animation's sake
        usleep(5000);
    }

    // Close log
    fclose(file);

    // Success
    return 0;
}

// Clears screen using ANSI escape sequences
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}

// Greets player
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(200000);
}

// Initializes the game's board with tiles numbered 1 through d*d - 1
// (i.e., fills 2D array with values but does not actually print them)
void init(void)
{
    // Checks if uneven tile count, and calculates num tiles
    int unplayable = d * d % 2;
    int tile_num = d * d - 1;
    // From top to bottom loop
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            // Completes the board if uneven tiles and at tile_num 2
            if (unplayable == 0 && tile_num == 2)
            {
                board[i][j] = 1;
                board[i][j + 1] = 2;
                board[i][j + 2] = 0;
                break;
            }

            board[i][j] = tile_num;
            tile_num--;

        }
    }
}

// Prints the board in its current state
void draw(void)
{
    // Loops though board
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            // Prints numbers single or double digits or blanks,
            // (tile number doens't exceed 80)
            if (board[i][j] != 0 && board[i][j] < 10)
            {
                printf(" %i ", board[i][j]);
            }
            else if (board[i][j] != 0)
            {
                printf("%i ", board[i][j]);
            }
            else
            {
                printf(" _ ");
            }
        }
        // New line after every row
        printf("\n");
    }
}

// If tile borders empty space, moves tile and returns true, else returns false
bool move(int tile)
{
    int tile_pos[2];
    int zero_pos[2];

    // loops though board, to find position of zero and choosen tile
    // (Liniear search)
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            if (board[i][j] == tile)
            {
                tile_pos[0] = i;
                tile_pos[1] = j;
            }
            else if (board[i][j] == 0)
            {
                zero_pos[0] = i;
                zero_pos[1] = j;
            }
        }
    }

    // checks if positions are only one tile apart
    int diff = abs(zero_pos[0] - tile_pos[0]) + abs(zero_pos[1] - tile_pos[1]);

    // Moves tile if moveable
    if (diff == 1)
    {
        board[zero_pos[0]][zero_pos[1]] = tile;
        board[tile_pos[0]][tile_pos[1]] = 0;
        return true;
    }
    else
    {
        return false;
    }
}

// Returns true if game is won (i.e., board is in winning configuration), else false
bool won(void)
{
    // Checks if order is correct and complete, if so you win.
    int tile_num = 1;
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            // if a single tile is out of order, stops immidiatly
            if (board[i][j] != tile_num)
            {
                return false;
            }
            if (tile_num == d * d - 1)
            {
                break;
            }
            tile_num++;
        }
    }
    return true;
}
