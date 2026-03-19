#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);

    for (int r = 1 ; r <= h ; r++) //creates selected amount of rows
    {

        for (int d = 0; d < h - r; d++) //creates spaces
        {
            printf(" ");

        }
        for (int c = 0 ; c < r ; c++) //creates number of hash based on r
        {
            printf("#");
        }
        printf("\n");
    }


}