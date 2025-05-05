#!/bin/bash
PORT=8502  # This is for Streamlit, NOT DeepSeek server

# Kill any leftover Streamlit process
PID=$(lsof -ti tcp:$PORT)
if [ ! -z "$PID" ]; then
  echo "Killing Streamlit process on port $PORT (PID $PID)..."
  kill -9 $PID
fi

# Run Streamlit
echo "Starting Streamlit on port $PORT..."
streamlit run main.py --server.port $PORT
