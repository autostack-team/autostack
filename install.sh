#!/bin/bash

sudo cp -r AutoStack /usr/bin/
sudo chmod +x /usr/bin/AutoStack/autostack.py
export PATH=$PATH:/usr/bin/AutoStack/
echo "function autostack() { 
    autostack.py;
    }" >> ~/.bashrc
source ~/.bashrc
