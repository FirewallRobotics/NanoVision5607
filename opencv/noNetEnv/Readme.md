
Bootstrap a pip installation on the target machine
Download a pip wheel distribution on an internet-connected machine from PyPI
Transfer it to the target machine
Install with $ python pip-21.3.1-py3-none-any.whl/pip install pip-21.3.1-py3-none-any.whl
Install python-cscore and it’s dependencies
Download all the dependencies that you need on a internet-connected machine
Transfer them to the target machine
Install with $ python -m pip install <whatever>



This is how I handle this case:

On the machine where I have access to Internet:

mkdir keystone-deps
pip download python-keystoneclient -d "/home/aviuser/keystone-deps"
tar cvfz keystone-deps.tgz keystone-deps
Then move the tar file to the destination machine that does not have Internet access and perform the following:

tar xvfz keystone-deps.tgz 
cd keystone-deps
pip install python_keystoneclient-2.3.1-py2.py3-none-any.whl -f ./ --no-index
You may need to add --no-deps to the command as follows:

pip install python_keystoneclient-2.3.1-py2.py3-none-any.whl -f ./ --no-index --no-deps