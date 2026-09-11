CC = gcc
NAME = sdl_app

main: main.c
	$(CC) main.c -o $(NAME) -I/opt/homebrew/include/SDL3 -D_THREAD_SAFE -L/opt/homebrew/opt/sdl3/lib -lSDL3 -Wl,-framework,Cocoa

clean:
	rm -f $(NAME)   