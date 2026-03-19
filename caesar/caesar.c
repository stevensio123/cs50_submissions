#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
// c[i]=(p[i]+k)%26--> remainder when divided by 26, to wrap around the values when its over 26.
//k is the secret key, a non negative int
//c[i] is the ciphered text
//p[i] is the normal character

bool only_digits(string s);      //checks for digits only, s = the value inside argv
char rotate(int key, char text);

int main(int argc, string argv[])
{

    if (argc < 3 && argc > 1 && only_digits(argv[1]))                 //check if argument has only one index
    {

        int k = atoi(argv[1]);                  // k = key
        string ptext = get_string("plaintext:  ");   // ptext = plain text

        printf("ciphertext: ");
        int i = 0;
        char ctext[i];
        for (i = 0; i < strlen(ptext); i++)
        {
            ctext[i] = rotate(k, ptext[i]);            // ctext = cipher text
            printf("%c", ctext[i]);
        }
        printf("\n");
        return 0;

    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
bool only_digits(string s)     //checks if argv is a digit
{
    int i = 0;
    int n;
    for (n = 0; n < strlen(s); n++)
    {
        if (isdigit(s[n]))
        {
            i += 0;
        }
        else
        {
            i += 1;
        }
    }

    if (i != 0)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}
char rotate(int key, char text)       //Use only when alphabet letter
{
    if (text > 64 && text < 91)        //for upper case
    {
        int i = text - 65;                  //i is the letter counting from 0
        int k = (i + key) % 26;       //k = the actual key in a wrapped A-Z
        char c = k + 65;
        return c;
    }
    else if (text > 96 && text < 124)   //for lower case
    {
        int i = text - 97;                  //i is the letter counting from 0
        int k = (i + key) % 26;       //k = the actual key in a wrapped a-z
        char c = k + 97;
        return c;
    }
    else
    {
        return text;
    }
}