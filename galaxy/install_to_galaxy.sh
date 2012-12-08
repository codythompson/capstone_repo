if [ "$#" -ne "1" ];
then
    echo "USAGE: ./install_to_galaxy.sh <galaxy-dir>"
    echo "  galaxy-dir: The directory where galaxy is installed."
else
    cp -f tool_conf.xml $1/tool_conf.xml
    cp -f datatypes_conf.xml $1/datatypes_conf.xml
    cp -f images.py $1/lib/galaxy/datatypes/images.py
    rm -rf $1/tools/CTXTestTools
    cp -rf tools/CTXTestTools $1/tools/CTXTestTools
fi
