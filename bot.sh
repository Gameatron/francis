while true; do
    python main.py
    for i in {3..1}; do
        echo “Restarting in $i”
        sleep 1
    done
done