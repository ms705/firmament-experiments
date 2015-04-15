CC=clang
CFLAGS=-std=c99
OPTFLAGS=-O3

all: mem_stream cpu_spin

%: %.c
	$(CC) $(CFLAGS) $(OPTFLAGS) -o $@ $^

clean:
	rm mem_stream
	rm cpu_spin
