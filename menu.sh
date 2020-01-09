#!/bin/bash
# Bash Menu Script Example

# UI Variables
HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=4
BACKTITLE="SynapsETS"
TITLE="MICSA Data"
MENU="Choose one of the following options:"

menuOptions=("Log In" "Exit Program")
sessionOptions=("New Session" "Exit Session Menu")

#Processing variables
count = 600000  #600,000 millisecondes
start_time = 0    #début (timeout)
elapsed_time = 0  #temps écoulé (timeout)

CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${menuOptions[@]}" \
                2>&1 >/dev/tty)
clear

## FUNCTION DEFINITIONS

#Close application
function quit {
    exit
}

#Open session menu
function session {
    select opt in "${sessionOptions[@]}"
do
    case $opt in
        "New Session")
			aws kinesis create-stream --stream-name MicsaDataStreaming --shard-count 1
            runSession
			aws kinesis delete-stream --stream-name MicsaDataStreaming
            ;;
        "Exit Session Menu")
            echo "Back to main menu"
            echo "1) Log In"
            echo "2) Exit Program"
            return
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done
}

#Begin recording session
function runSession {
    
    echo "New session is in progress. Serial data is being recorded."
    while [ 1 ]
    do
        read -n1 -r -p "Press S to start and T to terminate " key
    done
    ( if [ "$key" == "s" ]; then
        echo "You're in!"
		while [ $elapsed_time -lt $count ]; do
        echo "Made it past while loop condition"
		READ=`dd if=/dev/ttyUSB0 time = 600 | sed 's/ /*/g'`
		DATA=$(echo $READ | sed 's/ /,/g')
		aws kinesis put-record --stream-name MicsaDataStreaming --data $DATA --partition-key data
		echo "$DATA"
		#Long-term, we could use the optional --sequence-number-for-ordering parameter, which guarantees proper ordering of outgoing data
        if [ -z "$DATA" ] && [ "$elapsed_time" -eq 0 ]; then
            $start_time = date +%s%N | cut -b1-13
            $elapsed_time = $(((date +%s%N | cut -b1-13)-$start_time))
        elif [ -z "$DATA" ] && [ "$elapsed_time" -gt 0 ]; then
            $elapsed_time = $(((date +%s%N | cut -b1-13)-$start_time))
        else
            start_time = 0
            elapsed_time = 0
		fi
		done
	elif [ "$key" == "t" ]; then
		return
    else
        echo "Unknown"
    fi )
}

## START OF MAIN PROGRAM
select opt in "${menuOptions[@]}"
do
    case $opt in
        "Log In")
            echo "Please enter your username and password (a space between the two): "
            read existingUSN existingPW
            if grep -q "$existingUSN $existingPW" users.txt
            then
                echo "Successfully authenticated."
                echo "Session Menu:"
                session
            else
                echo "Invalid Credentials."
            fi
            ;;
        "Exit Program")
            quit
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done