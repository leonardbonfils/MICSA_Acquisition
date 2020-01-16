#!/bin/bash

# Choix de menus
menuOptions=("Log In" "Exit Program")
sessionOptions=("New Session" "Exit Session Menu")

# La variable $$ nous donne toujours le PID du processus actuel
echo "Processus parent demarre avec PID: $$"


## FUNCTIONS DEFINITIONS ##

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
			return
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
    #Function read user input continously
    echo "New session is in progress. Serial data is being recorded."
	while :
    do
		read -n1 -r -p "Press S to start and T to terminate" key
		if [ "$key" = "s" ]; then
			# La variable $! nous donne le PID du dernier sous-processus demarre
			# Le & a la fin de la commande demarre le processus en backgroup (donc en parallele)
			./menu_child.sh &
			CHILD_PID=$!
            echo "Processus child demarre avec PID: $CHILD_PID"
		elif [ "$key" = "t" ]; then
			# A la fin du programme il faut tuer le process child. Il ne se tue pas tout seul car le sous-process
			# qu'on a demarre dans le background n'est pas un sous-processus de parent.sh mais du shell. 
			kill $CHILD_PID
			#Stops AWS stream
			aws kinesis delete-stream --stream-name MicsaDataStreaming
			#Exit function
			echo "Recording terminated."
			return
		fi
	done
}




## START MAIN PROGRAM 
echo "Processus child demarre avec PID: $CHILD_PID"
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

echo "Execution du parent terminee"






