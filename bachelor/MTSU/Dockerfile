FROM ubuntu:16.04
MAINTAINER Alexander Karavaev

RUN apt-get update && \
    apt-get -y install tcl8.5 tk8.5 tcllib tclx8.4 libtk-img rxvt-unicode sdcc doxygen itcl3 bwidget tdom && \
    apt-get install -y mcu8051ide

CMD ["mcu8051ide"]