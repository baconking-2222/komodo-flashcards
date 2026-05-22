#!/bin/bash
# Launch the Komodo Wellbeing Flash Cards app.
# Usage: ./run.sh

cd "$(dirname "$0")"

# Check streamlit is installed; install if not.
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Streamlit not found — installing…"
    pip3 install -r requirements.txt
fi

echo "Opening the Komodo Flash Cards app in your browser…"
python3 -m streamlit run Browse_all.py
