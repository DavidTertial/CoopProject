#include <stdio.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>

int main(void)
{
    while (1) {
        time_t now = time(NULL);
        struct tm *t = localtime(&now);

        int hour = t->tm_hour;
        int minute = t->tm_min;
        int second = t->tm_sec;

        // Print time in HH:MM:SS format (24-hour clock)
        printf("\r%02d:%02d:%02d", hour, minute, second);
        fflush(stdout);

        sleep(1);
    }

    return 0;
}
