"""User-initiated handoff of approved text only; never send photos or call a model."""
import json
import streamlit as st


def handoff_html(prompt):
    payload = json.dumps(prompt, ensure_ascii=True).replace('<', '\\u003c')
    return '''<!doctype html><html lang="de"><meta charset="utf-8">
<style>body{font:15px Arial,sans-serif;color:#ece7df;background:#101318;margin:0;padding:8px}select,button,textarea{font:inherit;border:1px solid #666;border-radius:8px;padding:12px;box-sizing:border-box}select,textarea{width:100%;background:#20252d;color:#ece7df}button{background:#dbb678;color:#101318;cursor:pointer;margin:12px 8px 8px 0}button:disabled{opacity:.45;cursor:default}label{display:block;margin:12px 0;line-height:1.5}p{line-height:1.5;color:#c4c8d0}textarea{height:200px;margin-top:12px}a{color:#dbb678}:focus-visible{outline:3px solid #dbb678}</style>
<label for="provider">KI auswählen</label>
<select id="provider"><option value="chatgpt">ChatGPT (Text vorausgefüllt)</option><option value="gemini">Gemini (Text kopieren und einfügen)</option><option value="copilot">Microsoft Copilot (Text kopieren und einfügen)</option></select>
<p id="help"></p>
<label><input type="checkbox" id="consent"> Ich möchte den freigegebenen Prompt an den ausgewählten Dienst übergeben. Fotos füge ich dort selbst hinzu. Das ist keine Freigabe zur Bilderzeugung.</label>
<button id="open" disabled>An KI übergeben</button><button id="copy">Prompt kopieren</button>
<p id="status" role="status" aria-live="polite"></p>
<details><summary>Prompt zum manuellen Kopieren anzeigen</summary><textarea id="text" readonly aria-label="Vollständiger freigegebener Prompt"></textarea></details>
<p>Danach: Fotos als einzelne JPG-Dateien hinzufügen, Text prüfen und erst im KI-Chat die Bilderzeugung ausdrücklich freigeben. Eine Anmeldung und ein passendes Kontingent beim Anbieter können erforderlich sein.</p>
<script>
const prompt=__PAYLOAD__;
const provider=document.getElementById('provider'),consent=document.getElementById('consent'),openButton=document.getElementById('open'),status=document.getElementById('status');
const text=document.getElementById('text');text.value=prompt;
const destinations={chatgpt:'https://chatgpt.com/',gemini:'https://gemini.google.com/app',copilot:'https://copilot.microsoft.com/'};
function update(){consent.checked=false;openButton.disabled=true;status.textContent='';document.getElementById('help').textContent=provider.value==='chatgpt'?'ChatGPT öffnet in einem neuen Tab mit dem Text als Entwurf. Der Prompt wird dafür in der Linkadresse übertragen und kann im Browserverlauf stehen. Falls die Vorausfüllung nicht klappt, nutze „Prompt kopieren“.':'Der Chat öffnet in einem neuen Tab. Der Prompt wird zusätzlich in die Zwischenablage kopiert; füge ihn dort mit Strg+V oder langem Tippen ein. Eine automatische Vorausfüllung ist hier nicht eingerichtet.';}
provider.addEventListener('change',update);consent.addEventListener('change',()=>{openButton.disabled=!consent.checked;});
async function copy(){try{await navigator.clipboard.writeText(prompt);return true;}catch(e){text.closest('details').open=true;text.focus();text.select();return false;}}
document.getElementById('copy').addEventListener('click',async()=>{status.textContent=await copy()?'Prompt kopiert.':'Bitte den markierten Text manuell kopieren (Strg+C oder lang tippen).';});
openButton.addEventListener('click',async()=>{if(!consent.checked)return;const selected=provider.value;let url=destinations[selected];if(selected==='chatgpt'&&prompt.length<=16000)url+='?prompt='+encodeURIComponent(prompt);const win=window.open(url,'_blank');if(win)win.opener=null;const copied=await copy();status.textContent=(win?'KI-Chat geöffnet. ':'Bitte Pop-ups für diese App erlauben und erneut klicken. ')+(copied?'Prompt zusätzlich kopiert. Falls nötig dort einfügen.':'Falls nötig den markierten Prompt manuell kopieren und dort einfügen.')+' Fotos selbst hinzufügen; noch keine Bilderzeugung freigegeben.';});
update();
</script></html>'''.replace('__PAYLOAD__', payload)


def render_handoff(prompt):
    st.subheader('An KI übergeben')
    st.caption('Nur dein geprüfter Text wird übergeben. Deine aufgenommenen Fotos werden nicht automatisch übertragen.')
    st.iframe(handoff_html(prompt), height='content', tab_index=0,
              alt='Freigegebenen Prompt an eine ausgewählte KI übergeben')
