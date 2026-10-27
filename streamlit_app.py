"""Portrait Studio: text-only configuration with explicit export approval."""
import os
from portrait_visual import REFERENCE_IMAGE
from camera_section import render_camera
from job_presets import JOB_PRESETS, preset_answers, option_label
import time
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from portrait_core import (QUESTIONS, GUARD, build_prompt, export_prompt, fingerprint,
                           validate, valid_hash, verify_password)

st.set_page_config(page_title='Portrait Studio', page_icon='📷', layout='centered')

st.markdown("""<style>
.stApp {background:#fafaf8; color:#ece7df;}
.block-container {max-width:700px; padding:4.5rem 1rem 3rem;}
.ps-masthead {display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #34383c; padding:0 0 1rem; margin-bottom:1.4rem; color:#cfaa6d;}
.ps-masthead small {font-size:.66rem; letter-spacing:.12em;}
.ps-masthead strong {display:block; font-size:1.5rem; letter-spacing:.12em; line-height:1.35;}
.st-key-studio_shell {background:#101318; border-radius:22px; padding:14px 12px 22px; color:#ece7df;}
.st-key-studio_shell h1,.st-key-studio_shell h2,.st-key-studio_shell h3 {color:#ece3d2 !important; font-family:Arial,sans-serif; letter-spacing:-.02em;}
h1,h2,h3 {color:#34383c !important;}
label {color:#34383c !important;}
.st-key-studio_shell h3 {font-size:1.2rem !important; line-height:1.4;}
.st-key-studio_shell label {color:#d1d3d8 !important;}
.st-key-studio_shell [data-testid="stCaptionContainer"] {color:#b8bcc5;}
.st-key-studio_shell [data-testid="stVerticalBlockBorderWrapper"] {background:#20252d; border-color:#30353d; border-radius:14px;}
.stButton button,.stDownloadButton button {border-radius:10px; min-height:2.75rem;}
.stButton button[kind="primary"],.stDownloadButton button {background:#dbb678; color:#101318; border-color:#dbb678; font-weight:700;}
.stButton button[kind="primary"]:hover,.stDownloadButton button:hover {background:#ebcc99; color:#101318;}
.ps-studio-head {display:flex; align-items:center; gap:10px; padding:0 0 12px;}
.ps-aperture {color:#d9b36b; font-size:1.7rem;}
.ps-studio-head strong {display:block; font-size:1.45rem; line-height:1.2; letter-spacing:-.03em;}
.ps-studio-head small {font-size:.65rem; color:#c6baa2;}
.ps-preview {margin-left:auto; padding:3px 8px; border-radius:20px; background:#272b31; font-size:.67rem; font-weight:700;}
.ps-photo {position:relative; overflow:hidden; width:100%; aspect-ratio:638/359; border:1px solid #282f30; border-radius:13px; background:#20252a;}
.ps-photo img {position:absolute; width:108.62069%; max-width:none; height:auto; object-fit:fill; left:-3.76176%; top:-22.56267%;}
.ps-landing h2 {font-size:1.45rem !important; font-weight:700; margin:12px 0 7px; padding:0;}
.ps-landing p {color:#c4c8d0; font-size:.82rem; line-height:1.45; margin:0 0 12px;}
.ps-grid {display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px;}
.ps-tile {background:#23272e; padding:12px; border-radius:13px; min-height:90px; text-decoration:none !important; color:#f0f0f1 !important; display:block;}
.ps-tile:hover {background:#2d323a;}
.ps-tile .ps-icon {display:block; color:#d8b16a; font-size:1.25rem; margin-bottom:7px;}
.ps-tile strong {display:block; font-size:.81rem; margin-bottom:5px;}
.ps-tile small {color:#bfc3cb; font-size:.65rem; line-height:1.35; display:block;}
.ps-control {background:#23272e; border-radius:13px; margin-top:10px; padding:12px; font-size:.8rem;}
.ps-control strong {display:block; margin-bottom:9px;}
.ps-control strong span {color:#d8b16a; margin-right:8px;}
.ps-control p {margin:0; font-size:.73rem; color:#c4c8d0; line-height:1.5;}
.ps-photo-note {color:#959da8; font-size:.63rem; margin:6px 0 10px;}
.ps-config-title {border-top:1px solid #363b43; padding-top:20px; margin-top:20px;}
@media(max-width:480px) {.block-container {padding:4rem .55rem 2rem;} .ps-masthead strong {font-size:1.2rem;} .ps-masthead small {font-size:.55rem;} .ps-studio-head strong {font-size:1.2rem;} .ps-landing h2 {font-size:1.25rem !important;} .ps-tile {padding:10px;} .ps-tile strong {font-size:.75rem;}}
</style>""", unsafe_allow_html=True)



def revoke():
    st.session_state.pop('approved_digest', None)
    st.session_state['export_consent'] = False


def config_changed():
    revoke()
    for key in ('prompt_editor', 'source_digest'):
        st.session_state.pop(key, None)


def apply_job():
    job = st.session_state.get('job_preset')
    if job not in JOB_PRESETS:
        return
    for key, value in preset_answers(job).items():
        if key not in ('identity', 'notes', 'market'):
            st.session_state['q_' + key] = value
    config_changed()
    st.session_state['applied_job'] = job


def clear_session():
    for key in list(st.session_state):
        del st.session_state[key]


def setting(name):
    try:
        return st.secrets.get(name, os.environ.get(name, ''))
    except StreamlitSecretNotFoundError:
        return os.environ.get(name, '')


def authenticate():
    encoded = setting('APP_PASSWORD_HASH')
    if not valid_hash(encoded):
        st.error('Der private Zugang ist noch nicht eingerichtet. Bitte APP_PASSWORD_HASH in den Server-Secrets konfigurieren. Anleitung: README.md.')
        st.stop()
    now = time.time()
    if st.session_state.get('auth_config') != fingerprint(encoded) or now - st.session_state.get('last_active', 0) > 1800:
        clear_session()
        st.session_state.update(auth_config=fingerprint(encoded), last_active=now)
    if st.session_state.get('authenticated'):
        st.session_state['last_active'] = now
        return
    st.title('📷 Portrait Studio')
    st.subheader('Privater Zugang')
    remaining = max(0, int(st.session_state.get('locked_until', 0) - now) + 1)
    if remaining:
        st.warning(f'Bitte warte {remaining} Sekunden und versuche es danach erneut.')
    with st.form('login'):
        password = st.text_input('Zugangspasswort', type='password', max_chars=256, key='password_entry')
        submitted = st.form_submit_button('Anmelden', disabled=bool(remaining))
    if submitted and not remaining:
        if verify_password(password, encoded):
            clear_session()
            st.session_state.update(authenticated=True, auth_config=fingerprint(encoded), last_active=now)
            st.rerun()
        else:
            failures = st.session_state.get('failures', 0) + 1
            st.session_state.update(auth_config=fingerprint(encoded), last_active=now, failures=failures)
            if failures >= 5:
                st.session_state['locked_until'] = now + 60
            st.session_state['clear_password'] = True
            st.rerun()
    if st.session_state.pop('clear_password', False):
        # Clear on the next run before widget instantiation (handled below).
        st.error('Anmeldung fehlgeschlagen.')
    st.stop()


if st.session_state.get('clear_password'):
    st.session_state.pop('password_entry', None)
authenticate()

st.markdown('<header class="ps-masthead"><div><small>PROFESSIONAL AI PHOTOGRAPHY</small><strong>PORTRAIT STUDIO</strong></div><small>V1 · PROMPT STUDIO</small></header>', unsafe_allow_html=True)
with st.container(key='studio_shell'):
    st.markdown(f"""<section class="ps-landing">
    <div class="ps-studio-head"><span class="ps-aperture">◉</span><div><strong>PORTRAIT STUDIO</strong><small>Professional AI Photography</small></div><span class="ps-preview">PROMPT-VORSCHAU</span></div>
    <div class="ps-photo"><img src="{REFERENCE_IMAGE}" alt="Fotostudio mit Softboxen und Kamera, aus deiner bereitgestellten Designreferenz"></div>
    <div class="ps-photo-note">Studioansicht aus deiner Designreferenz · simmckiesphotography.com</div>
    <h2>Dein professionelles Profilfoto.</h2>
    <p>Für Bewerbungen, LinkedIn und berufliche Profile. Individuell konfiguriert, mit Fokus auf deine natürliche Wiedererkennbarkeit.</p>
    <div class="ps-grid">
    <a class="ps-tile" href="#referenzfotos"><span class="ps-icon">▧</span><strong>Fotos aufnehmen</strong><small>Mit Gesichtsrahmen und Lichttipps</small></a>
    <a class="ps-tile" href="#deine-einstellungen"><span class="ps-icon">☷</span><strong>11 Einstellungen</strong><small>Individuelle Auswahl</small></a>
    <a class="ps-tile" href="#deine-einstellungen"><span class="ps-icon">⌗</span><strong>Identität bewahren</strong><small>Gesichtstreue priorisieren</small></a>
    <a class="ps-tile" href="#deine-einstellungen"><span class="ps-icon">↓</span><strong>Bildprompt erhalten</strong><small>Geprüften Text herunterladen</small></a>
    </div>
    <div class="ps-control"><strong><span>♧</span>Kontrollierte Bilderzeugung</strong><p>Keine Bilderzeugung ohne ausdrückliche Freigabe. Du entscheidest über deine Fotos und deinen Prompt. Keine automatische Weitergabe an KI-Dienste.</p></div>
    </section>""", unsafe_allow_html=True)
    st.markdown('<div id="referenzfotos"></div>', unsafe_allow_html=True)
    render_camera()
    st.markdown('<h2 id="deine-einstellungen" class="ps-config-title">Deine 11 Einstellungen</h2>', unsafe_allow_html=True)
    st.button('Sitzungsdaten löschen und abmelden', on_click=clear_session)
    with st.expander('Datenschutz: Was passiert mit deinen Angaben?'):
        st.write('Deine Texte werden zur Verarbeitung an den Streamlit-Server übertragen und im Sitzungsspeicher gehalten. Diese App schreibt sie nicht in Dateien, Datenbanken oder eigene Protokolle. Die optionale Kameraansicht verarbeitet Fotos ausschließlich im Browser und lädt sie nicht zum Server hoch. Die Kamera benötigt deine Browserfreigabe. Namen, Kontaktdaten oder andere vertrauliche Angaben sind für den Prompt nicht nötig.')
        st.write('Die Schaltfläche zum Abmelden entfernt die von dieser App verwalteten Sitzungsdaten. Bereits heruntergeladene Dateien bleiben auf deinem Gerät. Eine sofortige vollständige Löschung aus Browser-, Infrastruktur- oder Serverspeicher wird nicht zugesichert. Bei Inaktivität wird die Anmeldung beim nächsten Zugriff nach 30 Minuten verworfen.')
        st.write('Lade aufgenommene Referenzfotos zuerst auf dein Gerät herunter und anschließend selbst im von dir gewählten Bilddienst hoch. Dessen Bedingungen und Datenschutzhinweise gelten dort gesondert. Nutze nur Fotos mit den erforderlichen Rechten und Einwilligungen. Betreiber- und Hosting-Angaben stehen unten, sofern konfiguriert.')
        st.caption('Der Passwortzugang ist ein geteilter Zugang ohne Benutzerkonten. Für öffentlich erreichbare Apps zusätzlich die Zugriffsverwaltung des Hosters nutzen.')

    st.subheader('Mit einer Job-Vorlage starten')
    st.selectbox('Job oder Berufsfeld', ['Ohne Vorlage / eigener Beruf'] + list(JOB_PRESETS), key='job_preset')
    st.caption('Wähle eine Vorlage und übernimm sie mit dem Button. Sie setzt die Auswahlfelder und die Berufsangabe neu; individuelle Auswahl-Details werden geleert. Persönliche Merkmale, Bewerbungsmarkt und weitere Wünsche bleiben erhalten. Danach ist alles frei anpassbar. Die Vorschläge sind keine Kleiderregeln; Berufskleidung oder Uniformen werden nicht automatisch ergänzt.')
    st.button('Job-Vorschlag übernehmen', on_click=apply_job, disabled=st.session_state.get('job_preset') not in JOB_PRESETS)
    if st.session_state.get('applied_job'):
        st.caption('Zuletzt übernommene Vorlage: ' + st.session_state['applied_job'] + '. Deine aktuellen Einstellungen darunter gelten für den Prompt.')

    answers = {}
    for key, label, options in QUESTIONS:
        with st.container(border=True):
            st.subheader(label)
            if options:
                answers[key] = st.selectbox('Auswahl', options, format_func=option_label, key='q_' + key, on_change=config_changed)
                answers[key + '_detail'] = st.text_input('Details (bei eigener Vorgabe erforderlich)', key='q_' + key + '_detail', max_chars=400, on_change=config_changed)
            else:
                help_text = ('Zum Beispiel: Data Analyst im Gesundheitswesen; keine Arbeitgebernamen nötig.' if key == 'context'
                             else 'Zum Beispiel: Brille und Sommersprossen erhalten. Alter und Gesichtsmerkmale bleiben grundsätzlich erhalten.')
                answers[key] = st.text_input('Deine Angaben (optional)', help=help_text, key='q_' + key, max_chars=400, on_change=config_changed)
            if key == 'context':
                answers['market'] = st.text_input('Bewerbungsmarkt (optional)', key='q_market', max_chars=100, on_change=config_changed)
            if key == 'identity':
                answers['gender'] = st.selectbox(
                    'Geschlecht (optional)', ['Männlich', 'Weiblich', 'Neutral'],
                    index=None, placeholder='Bei Bedarf auswählen', key='q_gender',
                    format_func=lambda value: value + {
                        'Männlich': ' (männliche Selbstbeschreibung)',
                        'Weiblich': ' (weibliche Selbstbeschreibung)',
                        'Neutral': ' (ohne geschlechtsspezifische Vorgaben)',
                    }[value], on_change=config_changed)
                st.caption('Deine freiwillige Angabe wird in den Prompt übernommen. Gesichtszüge und Identität bleiben erhalten. Job-Vorlagen verändern diese Auswahl nicht.')
            if key == 'composition':
                answers['gaze'] = st.selectbox('Blickrichtung', ['Direkt in die Kamera', 'Leicht versetzt', 'Dezent seitlich'], format_func=option_label, key='q_gaze', on_change=config_changed)
            if key == 'variants':
                answers['formats'] = st.selectbox('Ausgabeformate', ['4:5 und 1:1', '4:5', '3:4', '1:1'], format_func=option_label, key='q_formats', on_change=config_changed)
    answers['notes'] = st.text_area('Weitere Wünsche (optional)', key='q_notes', max_chars=1200, on_change=config_changed)

    if st.button('Prompt-Vorschau erstellen', type='primary'):
        revoke()
        errors = validate(answers)
        if errors:
            for error in errors:
                st.error(error)
        else:
            st.session_state['prompt_editor'] = build_prompt(answers)
            st.session_state['source_digest'] = fingerprint(repr(answers))

    if 'prompt_editor' in st.session_state:
        st.divider()
        st.subheader('Prompt prüfen und Export freigeben')
        st.caption('Änderungen an Antworten oder Prompt heben die Exportfreigabe auf. Neue Antworten erfordern eine neue Vorschau.')
        st.code(GUARD, language=None)
        body = st.text_area('Bearbeitbarer Prompt', key='prompt_editor', height=450, max_chars=16000, on_change=revoke)
        full_prompt = export_prompt(body)
        digest = fingerprint(full_prompt)
        st.checkbox('Ich habe diesen Text geprüft und gebe ausschließlich den TXT-Export frei. Eine Bilderzeugung erfordert später meine separate Zustimmung im Bild-KI-Chat.', key='export_consent', on_change=lambda: st.session_state.pop('approved_digest', None))
        if st.button('Diesen Prompt zum Export freigeben', disabled=not (st.session_state.get('export_consent') and body.strip())):
            st.session_state['approved_digest'] = digest
        approved = st.session_state.get('approved_digest') == digest and st.session_state.get('export_consent')
        if approved:
            st.success('Text zum Export freigegeben. Es wurden keine Bilder erzeugt.')
            st.download_button('Geprüften Prompt als TXT herunterladen', full_prompt.encode('utf-8'), file_name='portrait-studio-prompt.txt', mime='text/plain')
            st.caption('Zum Kopieren kannst du den vollständigen Exporttext aufklappen. Der feste Freigabehinweis wird immer mit exportiert.')
            with st.expander('Vollständigen Exporttext kopieren'):
                st.code(full_prompt, language=None)

    st.divider()
    st.caption('Portrait Studio · Textvorbereitung · Keine integrierte Bilderzeugung')
    operator = setting('OPERATOR_NOTICE')
    if operator:
        st.text(operator)
    else:
        st.caption('Betreiber- und Datenschutzkontakt noch nicht hinterlegt. Vor Veröffentlichung ergänzen.')
