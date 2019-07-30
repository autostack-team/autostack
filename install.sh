development=
while getopts d switch
do
     case $switch in
     d) development=1;;
     ?) printf "Usage: %s: [-d]\n"  $0; exit 2;;
     esac
done

if [ $development ]; then
    pip3 install -e .[development]
else 
    pip3 install -e .
fi
