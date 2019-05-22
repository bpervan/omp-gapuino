#include <stdlib.h>
#include <stdio.h>

int main()
{
    int a=0;
    for(int i=0;i<10;i++)
    {
        if(++a%2==0)
            
            printf("valor de i:%d valor de a:%d\n",i,a);
    }
    a=0;
    for(int i=0;i<10;i++)
    {
        if(a++%2==0)
            printf("valor de i:%d valor de a:%d\n",i,a);
    }


}
