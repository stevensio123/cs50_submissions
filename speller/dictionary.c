// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>

#include "dictionary.h"


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 187751; //odd prime number

// Hash table
node *table[N];
// size
int words = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO

    int n = hash(word);

    for (node *cursor = table[n]; cursor != NULL; cursor = cursor->next) //iterate through table n
    {

        if (strcasecmp(cursor->word, word) == 0) //compare strings
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function

    //Used Data Structures youtube course of Dr. Rob Edwards from San Diego State University
    int hash = 0;
    /* int w = 0;
    //convert to upper case
    while (word[w] != '\0')
    {
        word[w] = tolower(word[w]);
        w++;
    }
    */
    for (int i = 0; i <= strlen(word); i++)
    {
        hash = (31 * hash + toupper(word[i])) % N; //31 because math
        //check hash size
        /*if (hash >= N)
            {
                printf("incorrect hash!");
            }*/
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    //open dictionary file
    FILE *file = fopen(dictionary, "r");

    if (file == NULL)
    {
        return 1;
    }
    char word[LENGTH + 1];
    //read one word at a time until EOF
    while (fscanf(file, "%s", word) != EOF)
    {
        node *tmp = malloc(sizeof(node));  //create new node for each word
        if (tmp == NULL)
        {
            return false;
        }

        strcpy(tmp -> word, word);
        tmp -> next = NULL;

        int n = hash(word);

        if (table[n] == NULL)
        {
            table[n] = tmp;
        }
        else
        {
            tmp -> next = table[n];
            table[n] = tmp;
        }
        words++;
    }

    /*
            while (table[n] -> word[0] != '\n')
            {
                table[n] = table[n] -> next;
            }
            if (table[n] -> word[0] == '\n')
            {
                strcpy (table[n] -> word, file_word);
                table[n] -> next = NULL;
            }

        }
    */
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO


    for (int n = 0; n < N; n++)
    {
        node *head = table[n];
        node *cursor = head;
        node *tmp = head;

        while (cursor != NULL)
        {
            cursor = cursor -> next;
            free(tmp);
            tmp = cursor;
        }
    }

    return true;
}
