#include <stdio.h>
#include <unistd.h>

void get_ASCII() {
    char c;
    printf("enter a character\n> ");
    scanf("%s", &c);

    int milliseconds = 250;

    usleep(milliseconds * 1000);
    printf("\nASCII value of %c is %d\n",c ,c);
    usleep(milliseconds * 1000);
}

int main() {
    get_ASCII();
    return 0;
}