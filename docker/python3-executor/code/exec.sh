#! /bin/sh

echo ""

whoami
echo "says hello world!"
echo "from Docker!"

echo ""

lsb_release -a
uname -a

echo ""

cat /etc/os-release

echo ""

os_id=$(grep "^\(ID\|id\)=" /etc/os-release | awk -F= '{print $2}')
echo "Detected OS ID: $os_id"
env_dir=env-$os_id

echo "System Python 3:"
python3 --version
if [ -d $env_dir ] ; then
    if [ -d $env_dir/bin ]; then
        if [ -f $env_dir/bin/python3 ]; then
            echo "VirtualEnv Python 3:"
            $env_dir/bin/python3 --version
        else
            echo "No VirtualEnv Python"
            rm -rdv $env_dir
        fi
    else
        echo "No VirtualEnv Bin"
        rm -rdv $env_dir
    fi
else
    echo "No VirtualEnv"
fi

echo ""

echo "=========================="
echo "| VirtualEnv Management: |"
echo "=========================="
if [ ! -d $env_dir ]; then
    echo "Creating VirtualEnv..."
    echo "----------------------"
	virtualenv --python=python3 $env_dir
    echo "-----------------------------------"
fi
echo "Installing Dependencies with Pip..."
echo "-----------------------------------"
$env_dir/bin/pip3 install -r requirements.txt

echo ""

echo "====================="
echo "| Executing Python: |"
echo "====================="
$env_dir/bin/python3 main.py
