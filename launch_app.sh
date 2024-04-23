#!/bin/bash
chmod +x launch_app.sh

echo "Select the launch mode for the model:"
echo "1. Server"
echo "2. Local"
echo "3. Api"
read -p "Enter choice [1-3]: " mode

case $mode in
    1)
        echo "Starting server..."
        python3 src/model_server.py &
        echo "Launching app in mode 1..."
        export method=server
        python3 src/Interface.py
        ;;
    2)
        echo "Launching app in mode 2..."
        export method=local
        python3 src/Interface.py
        ;;
    3)
        echo "Launching app in mode 3..."
        export method=api
        python3 src/Interface.py    
        ;;
    *)
        echo "Invalid option selected. Exiting."
        exit 1
        ;;
esac
