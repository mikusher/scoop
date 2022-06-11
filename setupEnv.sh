#!/bin/sh
# This script automates the creation of Python virtual environment.

# check if logs directory exists and create it if not
if [ ! -d "logs" ]; then
    # create logs directory
    echo "Creating logs directory..."
    mkdir logs
    echo "Logs directory created."
fi

# check if venv directory exists and create it if not
if [ -d "venv" ]; then
    echo "Virtual environment 'virtualenv' found, activating it."
else
    echo "Virtual environment not found, creating new 'virtualenv'."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "Virtual environment was successfully created."
    else
        echo "Virtual environment was NOT created, aborting."
        exit 1
    fi
fi

. venv/bin/activate
if [ $? -eq 0 ]; then
    echo "Virtual environment is successfully activated."
else
    echo "Virtual environment was NOT activated, aborting."
    exit 1
fi

echo "Installing required packages."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "All requirements were successfully installed."
else
    echo "Requirements were NOT installed properly, aborting."
    exit 1
fi

echo "Done."
echo "To activate the virtual environment, run 'source virtualenv/bin/activate'."
echo "To deactivate the virtual environment, run 'deactivate'."
echo "To run the application, execute 'python3 main.py'."
# break line
echo ""
# ask user if he wants to activate the virtual environment and run the application or just activate the virtual environment
echo "Do you want to activate the virtual environment and run the application or just activate the virtual environment?"
echo "1. Activate virtual environment and run application"
echo "2. Activate virtual environment only"
echo "3. Exit"
# read user input
read -p "Enter your choice [1-3]: " choice
# check if user input is valid
if [ $choice -lt 1 ] || [ $choice -gt 3 ]; then
    echo "Invalid choice, aborting."
    exit 1
fi
# run application if user wants to
if [ $choice -eq 1 ]; then
    echo "Running application."
    . venv/bin/activate
    python3 main.py
    if [ $? -eq 0 ]; then
        echo "Application was successfully run."
    else
        echo "Application was NOT run, aborting."
        exit 1
    fi
fi
# activate virtual environment if user wants to
if [ $choice -eq 2 ]; then
    echo "Activating virtual environment."
    . venv/bin/activate
    if [ $? -eq 0 ]; then
        echo "Virtual environment was successfully activated."
    else
        echo "Virtual environment was NOT activated, aborting."
        exit 1
    fi
fi
# exit if user wants to exit
if [ $choice -eq 3 ]; then
    echo "Exiting."
    exit 0
fi
# if user input is invalid, exit
echo "Invalid choice, aborting."
exit 1
# end of script
# Path: setupEnv.sh
#!/bin/sh
# This script automates the creation of Python virtual environment.