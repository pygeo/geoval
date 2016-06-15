rm -f mintrend.x
cython --embed mintrend.pyx
gcc -I/usr/include/python2.7 -o mintrend.x mintrend.c -lpython2.7 -lpthread -lm -lutil -ldl
./mintrend.x

#cython --embed test.pyx
#gcc -I/usr/include/python2.7 -o test.x test.c -lpython2.7 -lpthread -lm -lutil -ldl
#./test.x
