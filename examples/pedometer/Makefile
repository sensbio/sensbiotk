
all: obj/libPedometer.so

obj/libPedometer.so: pedometer.c pedometer.h countstep.c countstep.h freefall.c freefall.h
	gcc -shared pedometer.c freefall.c countstep.c -o obj/libPedometer.so -lm

clean: 
	rm obj/libPedometer.so
