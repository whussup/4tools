#!/bin/sh

########################################################################
#
# 4regen_pax_flags - regenerating default pax flags using paxctl-ng 
# and migrate-pax
#
# VERSION 0.0.1
#
# Idea / Written by Sebastian Vivian Gresser - All Rights Reserved
#
# Copyright (C) by geeBee UG (haftungsbeschränkt) - All Rights Reserved
# Copyright (C) by Sebastian Vivian Gresser - All Rights Reserved
#
########################################################################

#setting default PeMRS
migrate-pax -v | grep FAIL > /var/tmp/.to_flag && sed -i -e "s/FAIL: //g" /var/tmp/.to_flag && paxctl-ng -PeMRS $(</var/tmp/.to_flag) && rm -rf /var/tmp/.to_flag

########################## misc flags ##################################
#
# these flags need to be set when you want to use a configured Grsec/Pax 
# core with:
#

#qt desktop

paxctl-ng -m /usr/bin/firefox
paxctl-ng -m /usr/bin/plasmashell
paxctl-ng -m /usr/bin/kmail
paxctl-ng -m /usr/bin/sddm-greeter
paxctl-ng -m /usr/bin/kwin_x11
paxctl-ng -m /usr/lib64/libexec/kscreenlocker-greet
paxctl-ng -m /usr/lib64/libexec/ksmserver-logout-greeter
paxctl-ng -m /usr/lib64/libexec/ksmserver-switchuser-greeter
paxctl-ng -m /usr/bin/ksplashqml
paxctl-ng -m /usr/bin/systemsettings5

#gtk desktop
#...

#misc
#...

