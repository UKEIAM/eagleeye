#!/bin/sh
streamlit run --server.fileWatcherType=none src/eagleeye/main.py -- --models $1
