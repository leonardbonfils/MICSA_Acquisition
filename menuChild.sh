#!/bin/bash

#Processing variables
count=600000  #600,000 millisecondes
start_time=0    #début (timeout)
elapsed_time=0  #temps écoulé (timeout)

# Fonction qui s'execute lorsque le process child a recu un signal d'arret par le parent
# Utiliser cette fonction pour faire le menage au besoin...
function arreter_processus()
{
    echo ">> Signal d'interruption du child recu"
    # Ne pas oublier de sortir du script child a la fin
    exit
}

# Cette commande intercepte le signal envoye par la commande "kill" du parent. Lorsque le signal
# est intercepté, la fonction arreter_processus est appelee.
trap arreter_processus SIGTERM


# On releve le ID du parent
PARENT_PID=$(ps $$ -o ppid=)
echo ">> Processus child démarre avec PID : $$, le PID du parent $PARENT_PID"

# boucle infinie (pour simuler les releves a partir de USB0
while [ "$elapsed_time" -lt "$count" ]; do
	#Keep track of length of time without an input read
	READ=`dd if=/dev/ttyUSB0 time = 600 | sed 's/ /*/g'`
	DATA=$(echo $READ | sed 's/ /,/g')
	aws kinesis put-record --stream-name MicsaDataStreaming --data $DATA --partition-key data
	echo "$DATA"
	#Long-term, we could use the optional --sequence-number-for-ordering parameter, which guarantees proper ordering of outgoing data
    if [ -z "$DATA" ] && [ "$elapsed_time" -eq 0 ]; then
            $start_time=$SECONDS
			sleep 1
            $elapsed_time=$(($SECONDS - $start_time))
        elif [ -z "$DATA" ] && [ "$elapsed_time" -gt 0 ]; then
            $elapsed_time=$(($SECONDS-$start_time))
        else
            $start_time=0
            $elapsed_time=0
	fi
done

arreter_processus


# Supposons que le processus child se termine, si il faut aussi que le parent se termine: 
# kill $PARENT_PID
