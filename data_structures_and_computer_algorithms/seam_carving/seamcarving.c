/*
Seam Carving
Authors: Michael Guerzhoy (starter code), Tanvi Manku (completed functions), and Anna Chen (completed functions)
*/

//#include "c_img.c"
//#include "c_img.h"
#include <math.h>
#include "seamcarving.h" //remove for local compiling

double min(double a, double b, double c)
{
  double min = 0;
  if (b <= c && b <= a)
  {
    min = b;
  }
  else if (c <= b && c <= a)
  {
    min = c;
  }
  else
  {
    min = a;
  }
  return min;
}

double min_2(double a, double b)
{
  if (b < a)
  {
    return b;
  }
  else
  {
    return a;
  }
}

int find_min1(int a, int b, int c, double *best)
{
  int min = a;
  if (best[b] <= best[a] && best[b] <= best[c])
  {
    min = b;
  }
  else if (best[c] <= best[b] && best[c] <= best[a])
  {
    min = c;
  }
  return min;
}

int find_min2(int a, int b, double *best)
{
  if (best[b] < best[a])
  {
    return b;
  }
  else
  {
    return a;
  }
}

void calc_energy(struct rgb_img *im, struct rgb_img **grad)
{
  int rx, ry, gx, gy, bx, by;
  int left_x, right_x, top_y, bot_y;
  double delta_x_sq, delta_y_sq;
  double energy;
  uint8_t dg_energy;

  create_img(grad, im->height, im->width);

  for (int x = 0; x < im->width; x++)
  {
    for (int y = 0; y < im->height; y++)
    {
      left_x = x - 1;
      right_x = x + 1;
      top_y = y - 1;
      bot_y = y + 1;

      if (x == 0)
      {
        left_x = (im->width) - 1;
      }
      else if (x == (im->width) - 1)
      {
        right_x = 0;
      }

      if (y == 0)
      {
        top_y = (im->height) - 1;
      }
      else if (y == (im->height) - 1)
      {
        bot_y = 0;
      }

      rx = (int)get_pixel(im, y, right_x, 0) - (int)get_pixel(im, y, left_x, 0);
      gx = (int)get_pixel(im, y, right_x, 1) - (int)get_pixel(im, y, left_x, 1);
      bx = (int)get_pixel(im, y, right_x, 2) - (int)get_pixel(im, y, left_x, 2);

      ry = (int)get_pixel(im, bot_y, x, 0) - (int)get_pixel(im, top_y, x, 0);
      gy = (int)get_pixel(im, bot_y, x, 1) - (int)get_pixel(im, top_y, x, 1);
      by = (int)get_pixel(im, bot_y, x, 2) - (int)get_pixel(im, top_y, x, 2);

      delta_x_sq = (rx * rx) + (gx * gx) + (bx * bx);
      delta_y_sq = (ry * ry) + (gy * gy) + (by * by);

      energy = sqrt(delta_x_sq + delta_y_sq);
      energy = energy / 10;
      dg_energy = (uint8_t)(energy);

      set_pixel(*grad, y, x, dg_energy, dg_energy, dg_energy);
    }
  }
}

void dynamic_seam(struct rgb_img *grad, double **best_arr)
{

  *best_arr = malloc(grad->width * grad->height * (sizeof(double *)));

  // initialize the first row
  for (int first = 0; first < grad->width; first++)
  {
    (*best_arr)[first] = get_pixel(grad, 0, first, 0);
  }

  for (int i = 0; i < grad->height; i++)
  {
    for (int j = 0; j < grad->width; j++)
    {
      double smallest = 0;

      // Case: Beginning of row
      if (j == 0)
      {
        smallest = min_2((*best_arr)[(i - 1) * grad->width + j + 1],
                         (*best_arr)[(i - 1) * grad->width + j]);
      }

      // Case: End of row
      else if (j == grad->width - 1)
      {
        smallest = min_2((*best_arr)[(i - 1) * grad->width + j - 1],
                         (*best_arr)[(i - 1) * grad->width + j]);
      }

      else
      {
        smallest = min((*best_arr)[(i - 1) * grad->width + j - 1],
                       (*best_arr)[(i - 1) * grad->width + j],
                       (*best_arr)[(i - 1) * grad->width + j + 1]);
      }

      (*best_arr)[i * grad->width + j] = get_pixel(grad, i, j, 0) + smallest;
    }
  }
}

void recover_path(double *best, int height, int width, int **path)
{
  int index = 0;
  *path = malloc((height - 1) * sizeof(int));
  double min_cost = best[width * (height - 1)];
  for (int i = 0; i < width; i++)
  {
    if (best[width * (height - 1) + i] < min_cost)
    {
      min_cost = best[(width) * (height - 1) + i];
      index = i;
    }
  }

  (*path)[height - 1] = index;//best[width * (height - 1) + index];

  for (int j = height - 2; j >= 0; j--)
  {

    if (index == 0)
    {
      index = find_min2(j * width, j * width + 1, best) - j * width;
      (*path)[j] = index;//best[width * j + index];
    }
    else if (index == width - 1)
    {
      index = find_min2(j * width, j * width - 1, best) - j * width;
      (*path)[j] = index;//best[width * j + index];
    }

    else
    {
      index = find_min1(j * width + index, j * width + index + 1, j * width + index - 1, best) - j * width;
      (*path)[j] = index;//best[width * j + index];
    }
  }
}

void remove_seam(struct rgb_img *src, struct rgb_img **dest, int *path)
{
  create_img(dest, src->height, src->width - 1);

  for (int y = 0; y < src->height; y++)
  {
    for (int x = 0; x < src->width; x++)
    {
      if (x < path[y])
      {
        set_pixel(*dest, y, x, get_pixel(src, y, x, 0), get_pixel(src, y, x, 1), get_pixel(src, y, x, 2));
      }
      else if (x > path[y])
      {
        set_pixel(*dest, y, x - 1, get_pixel(src, y, x, 0), get_pixel(src, y, x, 1), get_pixel(src, y, x, 2));
      }
    }
  }
}


int main(void)
{

    struct rgb_img *im;
    struct rgb_img *cur_im;
    struct rgb_img *grad;
    double *best;
    int *path;

    read_in_img(&im, "HJoceanSmall.bin"); // HJoceanSmall.bin not included in GitHub project
    
    for(int i = 0; i < 400; i++){
        printf("i = %d\n", i);
        calc_energy(im,  &grad);
        dynamic_seam(grad, &best);
        recover_path(best, grad->height, grad->width, &path);
        remove_seam(im, &cur_im, path);

        char filename[200];
        sprintf(filename, "img%d.bin", i);
        write_img(cur_im, filename);


        destroy_image(im);
        destroy_image(grad);
        free(best);
        free(path);
        im = cur_im;
    }
    destroy_image(im);

}
