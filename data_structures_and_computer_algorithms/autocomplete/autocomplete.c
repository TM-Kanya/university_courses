/*
Autocomplete

Authors: Michael Guerzhoy (starter code), Tanvi Manku (completed functions), and Anna Chen (completed functions)
*/

#include "autocomplete.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
 * Function:  compare_lexo
 * --------------------
 * compares two terms in ascending lexographic order (A -> Z). Compares by weight if they are the same string
 *
 *  *comp_1: pointer to a term to compare
 *  *comp_2: pointer to a term to compare to
 *
 *  returns: the value of strcmp of the two terms
 *           returns the difference of the terms' weights if the terms are the same
 *           (int)
 */

int compare_lexo(const void *comp_1, const void *comp_2)
{
    int mag = strcmp(((term *)comp_1)->term, ((term *)comp_2)->term);

    if (mag != 0)
    {
        return mag;
    }
    else
    {
        return (((term *)comp_1)->weight - ((term *)comp_2)->weight);
    }
}

/*
 * Function:  compare_weight
 * --------------------
 * compares two terms by weight. Compares by ascending lexographic order (A -> Z) if the weighting is the same
 *
 *  *com_1: pointer to a term to compare
 *  *com_2: pointer to a term to compare to
 *
 *  returns: the difference of the terms' weights
 *           returns the value of strcmp if the weights are the same
 *           (int)
 */

int compare_weight(const void *com_1, const void *com_2)
{
    double mag = ((term *)com_2)->weight - ((term *)com_1)->weight;

    if (mag == 0)
    {
        int val = strcmp(((term *)com_1)->term, ((term *)com_2)->term);
        return val;
    }
    else if (mag < 0)
    {
        return -1;
    }
    else if (mag > 0)
    {
        return 1;
    }

    return mag;
}

/*
 * Function:  mod_term
 * --------------------
 *  copies string pointed to by b to a
 *
 *  *a: pointer to where string is to be copied
 *  *b: pointer to where string is to be copied from
 *
 *  returns: nothing
 */

void mod_term(term *a, const char *b)
{
    strncpy(a->term, b, sizeof(a->term) - 1);
    a->term[sizeof(a->term) - 1] = '\0';
}

/*
 * Function:  read_in_terms
 * --------------------
 *  stores data from a file as terms.
 *
 *  **terms: pointer to a pointer to store terms
 *  *pnterms: pointer to store the number of terms
 *  *filename: pointer to the name of the file to be read
	       this file should be in a format similar to wiktionary.txt,
	       where the first line is the total number of words in the file,
	       and each line after has a weight and respective word seperated by a tab. 
 *
 *  returns: nothing
 */

void read_in_terms(term **terms, int *pnterms, char *filename)
{
    
    FILE *fp = fopen(filename, "r");
    int count = 0;
    int maximum = 0;
    char line[200];

    fgets(line, sizeof(line), fp);
    *pnterms = atoi(line);

    *terms = (term *)malloc(*pnterms * sizeof(term));

    int value = 0;
    char *name;
    char *number;

    while (fgets(line, sizeof(line), fp) != NULL)
    {
        line[strlen(line) - 1] = '\0';
        number = strtok(line, "\t");
        ((*terms)[value]).weight = atof(number);

        name = strtok(NULL, "\t");
        mod_term(&(*terms)[value], name);

        value++;
    }
    fclose(fp);

    qsort(*terms, *pnterms, sizeof(term), compare_lexo);
}

/*
 * Function: lowest_match
 * --------------------
 * finds the index in terms of the first term in lexicographic ordering that matches the string substr
 *
 *  *terms: terms
 *  nterms: number of terms in terms
 *  *substr: pointer to a string to search for
 *
 *  returns: index of first term matching substr
 *           (int)
 */

int lowest_match(term *terms, int nterms, char *substr)
{

    int low = 0;
    int high = nterms - 1;
    int mid;

    while (low <= high)
    {

        mid = (low + high) / 2;
        char to_compare[strlen(substr)];
        char to_comp[strlen(substr)];
        strncpy(to_compare, terms[mid].term, strlen(substr));
        to_compare[strlen(substr)] = '\0';
        int compare = strcmp(to_compare, substr);

        if (compare < 0)
        {
            low = mid + 1;
        }
        else if (compare > 0)
        {
            high = mid - 1;
        }
        else
        {
            if (mid == 0)
            {
                return mid;
            }
            strncpy(to_comp, terms[mid - 1].term, strlen(substr));
            to_comp[strlen(substr)] = '\0';
            if (strcmp(to_comp, substr) != 0)
            {
                return mid;
            }
            else
            {
                high = mid - 1;
            }
        }
    }
    return -1;
}

/*
 * Function: highest_match
 * --------------------
 * finds the index in terms of the last term in lexicographic ordering that matches the string substr
 *
 *  *terms: terms
 *  nterms: number of terms in terms
 *  *substr: pointer to a string to search for
 *
 *  returns: index of last term matching substr
 *           (int)
 */

int highest_match(struct term *terms, int nterms, char *substr)
{
    int low = 0;
    int high = nterms - 1;
    int mid;

    while (low <= high)
    {

        mid = (low + high) / 2;
        char to_compare[strlen(substr)];
        char to_comp[strlen(substr)];
        strncpy(to_compare, terms[mid].term, strlen(substr));
        to_compare[strlen(substr)] = '\0';
        int compare = strcmp(to_compare, substr);

        if (compare < 0)
        {
            low = mid + 1;
        }
        else if (compare > 0)
        {
            high = mid - 1;
        }
        else
        {
            if (mid == nterms - 1)
            {
                return mid;
            }
            strncpy(to_comp, terms[mid + 1].term, strlen(substr));
            to_comp[strlen(substr)] = '\0';
            if (strcmp(to_comp, substr) != 0)
            {
                return mid;
            }
            else
            {
                low = mid + 1;
            }
        }
    }
    return -1;
}

/*
 * Function: autocomplete
 * --------------------
 * finds the index in terms of the first term in lexicographic ordering that matches the string substr
 *
 *  **answer: pointer to a pointer to store answers
 *  *n_answer: pointer to number of answers
 *  *terms: terms
 *  nterms: number of terms in terms
 *  *substr: pointer to a string to search for
 *
 *  returns: nothing
 */

void autocomplete(term **answer, int *n_answer, term *terms, int nterms, char *substr)
{
    int start_index = lowest_match(terms, nterms, substr);
    int end_index = highest_match(terms, nterms, substr);

    if (start_index == -1 && end_index == -1)
    { 
        // checking if the substing has no matches
        *n_answer = 0;
        *answer = NULL;
    }
    else
    {
        *n_answer = end_index - start_index + 1;
        *answer = (term *)malloc(*n_answer * sizeof(term));
        for (int i = start_index; i <= end_index; i++)
        {
            (*answer)[i - start_index] = terms[i];
        }
    }

    qsort(*answer, *n_answer, sizeof(term), compare_weight);
}