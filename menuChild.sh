#!/bin/bash

# Fonction qui s'execute lorsque le process child a recu un signal d'arret par le parent
# Utiliser cette fonction pour faire le menage au besoin...
function arreter_processus()
{
    pkill -f producer.py
    #echo ">> Signal d'interruption du child recu"
    exit
}

# Cette commande intercepte le signal envoye par la commande "kill" du parent. Lorsque le signal
# est intercepté, la fonction arreter_processus est appelee.
trap arreter_processus SIGTERM


# On releve le ID du parent
# PARENT_PID=$(ps $$ -o ppid=) -- avec ou sans les '$$'
#echo ">> Processus child démarre avec PID : $$, le PID du parent $PARENT_PID"
python producer.py &
PYTHON_PID=$!
wait
