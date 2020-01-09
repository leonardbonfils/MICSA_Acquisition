#!/bin/bash

# La variable $$ nous donne toujours le PID du processus actuel
echo "Processus parent demarre avec PID: $$"

# La variable $! nous donne le PID du dernier sous-processus demarre
# Le & a la fin de la commande demarre le processus en backgroup (donc en parallele)
./child.sh &
CHILD_PID=$!

echo "Processus child demarre avec PID: $CHILD_PID"

# Ici j'ai mis une boucle mais supposons que ici va le menu
for i in {1..5} :
do
	echo "Je suis dans le parent"
	sleep 1
done

# A la fin du programme il faut tuer le process child. Il ne se tue pas tout seul car le sous-process
# qu'on a demarre dans le background n'est pas un sous-processus de parent.sh mais du shell. 
kill $CHILD_PID

echo "Execution du parent terminee"
