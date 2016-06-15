#rm -f mintrend.x/home/m300028/shared/dev/svn/geoval/geoval/statistic/build/temp.linux-x86_64-2.7

rm -rf ./build
rm mintrend.c
python setup_mintrend.py build_ext --inplace
cp ./build/temp.linux-x86_64-2.7/*.o .   # this is only done as in place compilation does somehow not work
python -c "from mintrend import *"


#cython --embed mintrend.pyx
#gcc -I/usr/include/python2.7 -o mintrend.x mintrend.c -lpython2.7 -lpthread -lm -lutil -ldl
#./mintrend.x

#cython --embed test.pyx
#gcc -I/usr/include/python2.7 -o test.x test.c -lpython2.7 -lpthread -lm -lutil -ldl
#./test.x
