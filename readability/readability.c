#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

//function names
int count_letters(string textinput);
int count_words(string wordcount);
int count_sentences(string sentencecount);
int main(void)
{
    string text = get_string("Text: ");
    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);

    float L = (letters / words) * 100;    // L = average letters
    float S = (sentences / words) * 100;  // S = average sentences
    float index = (0.0588 * L) - (0.296 * S) - 15.8; //finds the grade level

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index <= 16)
    {
        printf("Grade %.0f\n", round(index));   //round index to whole number if below 16
    }
    else
    {
        printf("Grade 16+\n");
    }
}


int count_letters(string lettercount) //counting letters from text
{
    int i;
    int letters_amount = 0;
    for (i = 0; i < strlen(lettercount); i++)
    {
        if (isalpha(lettercount[i]))
        {
            letters_amount += 1;
        }
        letters_amount += 0;
    }
    return letters_amount;
}
int count_words(string wordcount) //counting words from text
{
    int i;
    int word_amount = 1;
    for (i = 0; wordcount[i] != '\0'; i++)
    {
        if (wordcount[i] == 32)
        {
            word_amount += 1;
        }
    }
    return word_amount;
}
int count_sentences(string sentencecount) //counts sentences based on ., !, ?
{
    int i;
    int sentence_count = 0;
    for (i = 0; sentencecount[i] != '\0'; i++)
    {
        if (sentencecount[i] == 46 || sentencecount[i] == 33 || sentencecount[i] == 63)
        {
            sentence_count += 1;
        }
    }
    return sentence_count;
}