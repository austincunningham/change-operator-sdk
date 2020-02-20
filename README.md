# Change the Operator-sdk binary

Shell script for downloading an changeing the operator-sdk binary so you can manage mutliple binarys locally.  Symlinking to `/usr/local/bin/opeator-sdk` from `/opt/operator-sdk/<version>/operator-sdk`. Should work with linux and Mac

> *NOTE*: This script doesn't verify the operator-sdk binary. Haven't tested on Mac.

# Usasge

```sh
# Clone the Repo
git clone https://github.com/austincunningham/change-operator-sdk.git
# change directory 
cd change-operator-sdk
# Set the file to be able to execute
chmod +x choperator-sdk.sh 
# run the script
./choperator-sdk.sh
```
![](screenshot.png)

