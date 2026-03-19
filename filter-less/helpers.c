#include "helpers.h"
#include "math.h"


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    //RGBTRIPLE.rgbtBlue = ....
   for (int r = 0; r < height; r++)
   {
      for (int c = 0; c < width; c++)
      {
        float average = (image[r][c].rgbtRed + image[r][c].rgbtGreen + image[r][c].rgbtBlue) / 3.0;
        int avg = round(average);
        image[r][c].rgbtRed = avg;
        image[r][c].rgbtGreen = avg;
        image[r][c].rgbtBlue = avg;
      }
   }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for(int r = 0; r < height; r++)
    {
        for(int c = 0; c < width; c++)
        {
            float red = (image[r][c].rgbtRed * 0.393) + (image[r][c].rgbtGreen * 0.769) + (image[r][c].rgbtBlue * 0.189);
            float green = (image[r][c].rgbtRed * 0.349) + (image[r][c].rgbtGreen * 0.686) + (image[r][c].rgbtBlue * 0.168);
            float blue = (image[r][c].rgbtRed * 0.272) + (image[r][c].rgbtGreen * 0.534) + (image[r][c].rgbtBlue * 0.131);
            if(red > 255.0)
            {
                red = 255.0;
            }
            if (green > 255.0)
            {
                green = 255.0;
            }
            if (blue > 255.0)
            {
                blue = 255.0;
            }

            int Red = round(red);
            int Green = round(green);
            int Blue = round(blue);
            image[r][c].rgbtRed = Red;
            image[r][c].rgbtGreen = Green;
            image[r][c].rgbtBlue = Blue;

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE image2[height][width];
     for(int r = 0; r < height; r++)
     {
        int w = width - 1;
        for(int c = 0; c < width; c++)
        {
            image2[r][c].rgbtRed = image[r][w].rgbtRed;
            image2[r][c].rgbtGreen = image[r][w].rgbtGreen;
            image2[r][c].rgbtBlue = image[r][w].rgbtBlue;
            w = w - 1;
        }
    }
    for(int r = 0; r < height; r++)
    {
        for(int c = 0; c < width; c++)
        {
            image[r][c].rgbtRed = image2[r][c].rgbtRed;
            image[r][c].rgbtGreen = image2[r][c].rgbtGreen;
            image[r][c].rgbtBlue = image2[r][c].rgbtBlue;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
     RGBTRIPLE blur[height][width];
     int denominator;
     //loop for every image pixels
      for(int r = 0; r < height; r++)
      {
        for(int c = 0; c < width; c++)
        {
            float avgred = 0.0;
            float avggreen = 0.0;
            float avgblue = 0.0;
             //loop for pixels' surrounding pixels (box)
            for (int br = r - 1; br <= r + 1; br++)
            {
                for (int bc = c - 1; bc <= c + 1; bc++)
                {
                    //make sure pixels not over edge
                    while ((br >= 0) && (bc >= 0) && (br < height) && (bc < width))
                    {
                    avgred += image[br][bc].rgbtRed;
                    avggreen += image[br][bc].rgbtGreen;
                    avgblue += image[br][bc].rgbtBlue;
                    break;
                    }
                }
            }

            if (((r == 0) && (c == 0)) || ((r == height - 1) && (c == 0)) || ((r == 0) && (c == width - 1)) || ((r == height - 1) && (c == width - 1)))
            {
                denominator = 4;
            }
            else if (r == 0 || c == 0 || r == height - 1 || c == width - 1)
            {
                denominator = 6;
            }
            else
            {
                denominator = 9;
            }
            int red = roundf (avgred / denominator);
            int green = roundf (avggreen / denominator);
            int blue = roundf (avgblue / denominator);

            blur[r][c].rgbtRed = red;
            blur[r][c].rgbtGreen = green;
            blur[r][c].rgbtBlue = blue;

        }
      }
      for(int r = 0; r < height; r++)
      {
         for(int c = 0; c < width; c++)
         {
            image[r][c].rgbtRed = blur[r][c].rgbtRed;
            image[r][c].rgbtGreen = blur[r][c].rgbtGreen;
            image[r][c].rgbtBlue = blur[r][c].rgbtBlue;
         }
      }



    return;
}
