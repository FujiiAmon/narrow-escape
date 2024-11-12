import streamlit as st
from game import main_start, main_play, main_continue, main_end

flagc = False
flagp = main_start()
while flagp:
    flagc = main_play(flagc)
    if not flagc:
        flagp = main_continue()
    if flagc:
        main_end()
        break