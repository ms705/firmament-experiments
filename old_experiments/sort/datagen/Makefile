CAMIO_PATH = /mnt/dev/camio

all: datagen

datagen: datagen.c
	gcc -o $@ -I$(CAMIO_PATH)/include/ $< $(CAMIO_PATH)/bin/libcamio.a
