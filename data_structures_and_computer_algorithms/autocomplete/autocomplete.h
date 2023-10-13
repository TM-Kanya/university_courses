/*
Autocomplete

Authors: Michael Guerzhoy (starter code), Tanvi Manku (completed functions), and Anna Chen (completed functions)
*/

#if !defined(AUTOCOMPLETE_H)
#define AUTOCOMPLETE_H

typedef struct term {
  char term[200]; // Assume terms are not longer than 200
  double weight;
} term;

void read_in_terms(struct term **terms, int *pnterms, char *filename);
int lowest_match(struct term *terms, int nterms, char *substr);
int highest_match(struct term *terms, int nterms, char *substr);
void autocomplete(struct term **answer, int *n_answer, struct term *terms, int nterms, char *substr);

#endif