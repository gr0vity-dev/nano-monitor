#!/bin/sh

#Script to create and delete a virtualenv to keep dependencies separate from other projects 
# ./venv_python.sh create 
 # ./venv_python.sh delete

action=$1

if [ "$action" = "" ]; 
then
    rm -rf venv_python
    python3 -m venv venv_python
    . venv_python/bin/activate

    ./venv_python/bin/pip3 install wheel
    ./venv_python/bin/pip3 install -r ./requirements.txt   

    echo "A new virstaul environment was created. "


elif [ "$action" = "delete" ];
then 
    . venv_python/bin/activate
    deactivate    
    rm -rf venv_python

else
     echo "run ./setup_python_venv.sh  to create a virtual python environment"
     echo "or"
     echo "run ./setup_python_venv.sh delete  to delete the virstual python environment"
fi


