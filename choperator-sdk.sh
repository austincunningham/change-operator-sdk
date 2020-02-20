#!/bin/sh
clear
echo " "
echo " .d88b.  d8888b. d88888b d8888b.  .d8b.  d888888b  .d88b.  d8888b.        .d8888. d8888b. db   dD" 
echo ".8P  Y8. 88  \`8D 88'     88  \`8D d8' \`8b \`~~88~~' .8P  Y8. 88  \`8D        88'  YP 88  \`8D 88 ,8P'" 
echo "88    88 88oodD' 88ooooo 88oobY' 88ooo88    88    88    88 88oobY'        \`8bo.   88   88 88,8P"   
echo "88    88 88~~~   88~~~~~ 88\`8b   88~~~88    88    88    88 88\`8b   C8888D   \`Y8b. 88   88 88\`8b   "
echo "\`8b  d8' 88      88.     88 \`88. 88   88    88    \`8b  d8' 88 \`88.        db   8D 88  .8D 88 \`88." 
echo " \`Y88P'  88      Y88888P 88   YD YP   YP    YP     \`Y88P'  88   YD        \`8888Y' Y8888D' YP   YD "
echo " "
echo "########################################################################################"
echo Current version of operator-sdk
echo " "
ls -la /usr/local/bin/operator-sdk
echo " "
echo "########################################################################################"
echo "Versions of operator-sdk on the system"
echo " "
ls /opt/operator-sdk
echo " "
echo "Do you wish to download a new version y/n ?"
read yesno
if [[ $yesno == "y" || $yesno == "Y" ]]
then
	echo "Enter the release version you wish to download e.g. v0.15.2 ?"
	read version
	if [[ "$OSTYPE" == "linux-gnu" ]]
	then
	    echo "Linux detected"
	    curl -LO https://github.com/operator-framework/operator-sdk/releases/download/${version}/operator-sdk-${version}-x86_64-linux-gnu
	    chmod +x operator-sdk-${version}-x86_64-linux-gnu && sudo mkdir -p /opt/operator-sdk/$version && sudo cp operator-sdk-${version}-x86_64-linux-gnu /opt/operator-sdk/$version/operator-sdk && rm operator-sdk-${version}-x86_64-linux-gnu
    elif [[ "$OSTYPE" == "darwin"* ]] 
    then
    	echo "Mac detected"
    	curl -LO https://github.com/operator-framework/operator-sdk/releases/download/${version}/operator-sdk-${version}-x86_64-apple-darwin
    	chmod +x operator-sdk-${version}-x86_64-apple-darwin && sudo mkdir -p /opt/operator-sdk/$version && sudo cp operator-sdk-${version}-x86_64-apple-darwin /opt/operator-sdk/$version/operator-sdk && rm operator-sdk-${version}-x86_64-apple-darwin
    fi
fi
echo " "
echo "########################################################################################"
while [ -z "$version" ]
do
	echo "What version do you wish to install ?"
	read version
done

sudo rm /usr/local/bin/operator-sdk
sudo ln -s /opt/operator-sdk/$version/operator-sdk /usr/local/bin/operator-sdk
echo " "
echo "########################################################################################"
echo "Version installed :"
echo " "
operator-sdk version
echo " "
echo "########################################################################################"