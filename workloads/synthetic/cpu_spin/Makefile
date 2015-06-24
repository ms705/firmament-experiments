CC=clang
CFLAGS=-std=c99
OPTFLAGS=-O3

all: cpu_spin

%: %.c
	$(CC) $(CFLAGS) $(OPTFLAGS) -o $@ $^

clean:
	rm cpu_spin
