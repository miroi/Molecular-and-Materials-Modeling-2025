Avogadro2 on WSL 
================

get and unzip
~~~~~~~~~~~~~~
wget https://nightly.link/OpenChemistry/avogadrolibs/workflows/build_linux/master/Avogadro2-x86_64.AppImage.zip

unzip Avogadro2-x86_64.AppImage.zip ... inflating: Avogadro2-x86_64.AppImage

ldd Avogadro2-x86_64.AppImage ... not a dynamic executable

install mssing packages
~~~~~~~~~~~~~~~~~~~~~~~
sudo apt install libfuse2

launch
~~~~~~
./Avogadro2-x86_64.AppImage




