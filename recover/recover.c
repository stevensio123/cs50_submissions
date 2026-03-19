#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint8_t BYTE;
#define sizeof_block  (512 * sizeof(BYTE))

int main(int argc, char *argv[])
{
    if (argc < 2 || argc > 2)
    {
        printf ("invalid usage: ./recover [file name]\n");
        return 1;
    }

    //open memory card
    FILE *raw_file = fopen(argv[1], "r");
    BYTE buffer [512];
    char *filename = malloc (8 * sizeof (char));//filenames: ###.jpg
    int n = 0;
    FILE *img = NULL;
    while (fread(&buffer, 1, sizeof_block, raw_file) == sizeof_block) //read until reached end of file
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (n > 0) //checks if first its still on the first jpeg
            {
                if (img != NULL)
                {
                    fclose(img);
                }
            }
            sprintf(filename, "%03i.jpg", n);
            img = fopen(filename, "w");

            if (img != NULL)
            {
                fwrite(&buffer, 1, sizeof_block, img);
            }
            n++;
        }
        else
        {
            if (img != NULL)
            {
                fwrite(&buffer, 1, sizeof_block, img);
            }
        }

    }
    if (img != NULL)
    {
        fclose(img);
    }

    fclose(raw_file);
    free(filename);
    return 0;
}


