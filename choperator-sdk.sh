#!/bin/sh
# Usage:
# ./choperator-sdk.sh
# You can pass in cmd line args as well
# ./choperator-sdk.sh v1.12.0
#
export ARCH=$(case $(uname -m) in x86_64) echo -n amd64 ;; aarch64) echo -n arm64 ;; *) echo -n $(uname -m) ;; esac)
export OS=$(uname | awk '{print tolower($0)}')
version=$1
clear
echo "########################################################################################################"
echo " "
echo " .d88b.  d8888b. d88888b d8888b.  .d8b.  d888888b  .d88b.  d8888b.        .d8888. d8888b. db   dD" 
echo ".8P  Y8. 88  \`8D 88'     88  \`8D d8' \`8b \`~~88~~' .8P  Y8. 88  \`8D        88'  YP 88  \`8D 88 ,8P'" 
echo "88    88 88oodD' 88ooooo 88oobY' 88ooo88    88    88    88 88oobY'        \`8bo.   88   88 88,8P"   
echo "88    88 88~~~   88~~~~~ 88\`8b   88~~~88    88    88    88 88\`8b   C8888D   \`Y8b. 88   88 88\`8b   "
echo "\`8b  d8' 88      88.     88 \`88. 88   88    88    \`8b  d8' 88 \`88.        db   8D 88  .8D 88 \`88." 
echo " \`Y88P'  88      Y88888P 88   YD YP   YP    YP     \`Y88P'  88   YD        \`8888Y' Y8888D' YP   YD "
echo " "
echo "########################################################################################################"
echo Current version of operator-sdk
echo " "
ls -la /usr/local/bin/operator-sdk
echo " "
echo "########################################################################################################"
versionCheck=$(ls /opt/operator-sdk | grep "$version")
echo "Versions of operator-sdk on the system"
echo " "
ls /opt/operator-sdk

if [[ -z "$version" || -z "$versionCheck" ]]; then
	echo " "
	echo "Version not found "
	echo "- You haven't specified a version"
	echo "- Your entered version is not currently on the system"
	echo "- You have entered a invalid version"
	echo " "
	echo "Do you wish to download a new version y/n ?"
	read yesno
	if [[ $yesno == "y" || $yesno == "Y" ]]
	then
		echo "Enter the release version you wish to download e.g. v0.15.2 ?"
		read version
    	export ARCH=$(case $(uname -m) in x86_64) echo -n amd64 ;; aarch64) echo -n arm64 ;; *) echo -n $(uname -m) ;; esac)
		export OS=$(uname | awk '{print tolower($0)}')
		export OPERATOR_SDK_DL_URL=https://github.com/operator-framework/operator-sdk/releases/download/${version}
		curl -LO ${OPERATOR_SDK_DL_URL}/operator-sdk_${OS}_${ARCH}
		chmod +x operator-sdk_${OS}_${ARCH} && sudo mkdir -p /opt/operator-sdk/$version && sudo mv operator-sdk_${OS}_${ARCH} /opt/operator-sdk/$version/operator-sdk 
		echo " "
		echo "########################################################################################################"
		sudo rm /usr/local/bin/operator-sdk
		sudo ln -s /opt/operator-sdk/$version/operator-sdk /usr/local/bin/operator-sdk
		echo "########################################################################################################"
		echo "Version installed :"
		echo " "
		operator-sdk version
		echo " "
		echo "########################################################################################################"
		exit 0
	else
		unset version
	fi
fi

while [ -z "$version" ]
do
	echo "Enter one of the versions already on the system to install :"
	read version
	versionCheck=$(ls /opt/operator-sdk | grep "$version")
done

sudo rm /usr/local/bin/operator-sdk
sudo ln -s /opt/operator-sdk/$version/operator-sdk /usr/local/bin/operator-sdk
echo " "
echo "########################################################################################################"
echo "Version installed :"
echo " "
operator-sdk version
echo " "
echo "########################################################################################################"
