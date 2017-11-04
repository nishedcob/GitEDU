# run with `source activate.en.sh` 
ENV_DIR=env-en
if [ ! -d $ENV_DIR ]; then
	virtualenv --python=python3 $ENV_DIR
fi
source $ENV_DIR/bin/activate
pip3 install -r requirements.en.txt

