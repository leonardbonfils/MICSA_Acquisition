#!/bin/bash

# Choix de menus
menuOptions=("Log In" "Exit Program")
sessionOptions=("New Session" "Exit Session Menu")

# La variable $$ nous donne toujours le PID du processus actuel
printf "\n----- Processus parent demarre avec PID: $$ -----\n\n"


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
		stty -echo
		read -n1 -r -p "Press s to start and t to  : " key
		stty echo
		if [ "$key" = "s" ]; then
			# La variable $! nous donne le PID du dernier sous-processus demarre
			# Le & a la fin de la commande demarre le processus en backgroup (donc en parallele)
			./menuChild.sh &
			CHILD_PID=$!
            echo "Processus child demarre avec PID: $CHILD_PID"
            echo "Recording started"
		elif [ "$key" = "t" ]; then
			kill $CHILD_PID
			echo "Recording terminated."
			return
		fi
	done
}




## START MAIN PROGRAM 
select opt in "${menuOptions[@]}"
do
    case $opt in
        "Log In")
            printf "\nPlease enter your username: "
            read micsaUser
            printf "Please enter your password: "
            unset password;
            while IFS= read -r -s -n1 charInput; do
                if [[ -z $charInput ]]; then
                    if [[ -z $password ]]; then
                        printf "\nPlease enter a non-empty password: "
                    else
                        break;
                    fi
                else
                    echo -n '*'
                    password+=$charInput
                fi
            done
            ## Ici, nous devrons ajouter le calcul du hash du password rentré
            ## Puis, envoyer ce hash à la base de données de Patrick
            ## et analyser la réponse de la DB pour déterminer si l'utilisateur existe
            printf "\n----- Successfully authenticated. -----"
            printf "\n\nSession Menu:\n"
            session
            ;;
        "Exit Program")
            quit
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

echo "Execution du parent terminee"
