import streamlit as st
from utils.data_manager import DataManager
from functions.design import (
	apply_global_styles,
	render_page_intro,
	render_section_title,
	render_empty_state
)
from functions.aboubersicht import (
	load_abo_uebersicht_data,
	render_subscription_cards,
	render_total_subscription_sum,
	render_interval_summary
)


apply_global_styles()

st.title("Aboübersicht")

render_page_intro(
	"Deine Abos auf einen Blick",
	"Hier siehst du deine Abonnements und darunter eine klare Zusammenfassung nach Intervall."
)


dm = DataManager(
	fs_protocol='webdav',
	fs_root_folder="bmldjm"
)

if not st.session_state.get("authentication_status"):
	st.warning("Bitte zuerst anmelden")
	st.switch_page("app.py")


df = load_abo_uebersicht_data(dm)

if df is None or df.empty:
	render_empty_state(
		"Keine Abonnements vorhanden",
		"Füge zuerst ein Abo hinzu, damit hier deine Übersicht angezeigt wird."
	)
	st.stop()


render_section_title("Alle Abonnements")

render_subscription_cards(df)


st.divider()


render_section_title("Gesamtsumme aller Abos")

render_total_subscription_sum(df)


st.divider()


render_section_title("Zusammenfassung nach Intervall")

render_interval_summary(df)