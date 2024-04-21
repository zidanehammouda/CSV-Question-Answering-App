#!/bin/bash
chmod +x launch_app.sh

echo "Select the launch mode for the model:"
echo "1. Server"
echo "2. Api"
echo "3. Local"
read -p "Enter choice [1-3]: " mode

case $mode in
    1)
        echo "Starting server..."
        python3 src/model_server.py &
        echo "Launching app in mode 1..."
        python3 src/Interface.py server
        ;;
    2)
        echo "Launching app in mode 2..."
        python3 src/Interface.py api
        ;;
    3)
        echo "Launching app in mode 3..."
        python3 src/Interface.py local
        ;;
    *)
        echo "Invalid option selected. Exiting."
        exit 1
        ;;
esac
