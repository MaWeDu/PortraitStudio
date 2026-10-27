"""Camera UI is fully browser-side. Photo bytes are never returned to Python."""
from pathlib import Path
import streamlit as st


def camera_html():
    directory = Path(__file__).resolve().parent
    template = (directory / 'camera_ui.html').read_text(encoding='utf-8')
    utilities = (directory / 'camera_utils.js').read_text(encoding='utf-8')
    return template.replace('/*__CAMERA_UTILS__*/', utilities)


def render_camera():
    st.subheader('Referenzfotos mit deiner Kamera aufnehmen')
    st.caption('Mit Gesichtsrahmen, drei Blickrichtungen und Lichttipps. Die Fotos bleiben in diesem Browser; es gibt keinen automatischen Upload zu Streamlit, ChatGPT oder anderen KI-Diensten.')
    show = st.toggle('Kamerabereich öffnen', key='show_camera')
    if show:
        st.warning('Bitte lade deine Fotos herunter, bevor du diesen Bereich schließt, die Seite neu lädst oder dich abmeldest. Änderungen an der App können die Kameraansicht neu laden.')
        st.iframe(camera_html(), height='content', tab_index=0, alt='Lokale Fotoaufnahme mit Gesichtsrahmen und Lichttipps')
