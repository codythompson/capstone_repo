if [ "$#" -ne "1" ];
then
    echo "USAGE: ./install_to_galaxy.sh <galaxy-dir>"
    echo "  galaxy-dir: The directory where galaxy is installed."
else
    echo "Copying tool_conf.xml to $1/tool_conf.xml" 
    cp -f tool_conf.xml $1/tool_conf.xml

    echo "Copying datatypes_conf.xml to $1/datatypes_conf.xml" 
    cp -f datatypes_conf.xml $1/datatypes_conf.xml

    echo "Copying universe_wsgi.ini to $1/universe_wsgi.ini" 
    cp -f universe_wsgi.ini $1/universe_wsgi.ini

    echo "Copying images.py to $1/lib/galaxy/datatypes/images.py" 
    cp -f images.py $1/lib/galaxy/datatypes/images.py

    echo "Copying File Directory of images to $1/database/files/Isis" 
    rm -rf $1/database/files/Isis
    cp -rf File_Directory/Isis $1/database/files/Isis

    echo "Copying the directory and contents of /tools/CTXTestTools/ to $1/tools/CTXTestTools/" 
    rm -rf $1/tools/CTXTestTools
    cp -rf tools/CTXTestTools $1/tools/CTXTestTools
fi
