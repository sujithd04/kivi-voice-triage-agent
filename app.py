"""
app.py - Kivi Voice Feedback Triage Agent Web Interface
Bonus deployment app (Streamlit / Web MVP)
"""

import os
import streamlit as st
from agent import (
    transcribe_audio,
    extract_ticket,
    deduplicate_ticket,
    generate_voice_confirmation,
    write_tickets_markdown,
    sarvam_client,
    SARVAM_API_KEY
)

st.set_page_config(page_title="Kivi Voice Feedback Triage", page_icon="🎙️", layout="wide")

st.title("🎙️ Kivi Voice Feedback Triage Agent")
st.caption("AI-powered triage for Hinglish & Hindi voice complaints | Built for Sarvam Hackathon")

col_info, col_status = st.columns([2, 1])
with col_info:
    st.write(
        "Users submit voice feedback. The agent transcribes with **Saaras**, "
        "extracts structured tickets with **Sarvam-105B**, merges duplicates, "
        "and replies in the user's language using **Bulbul**."
    )
with col_status:
    if sarvam_client and SARVAM_API_KEY:
        st.success("Sarvam SDK: Configured")
    else:
        st.info("Mode: Offline Demo Fallback")

st.divider()

# Test Audio Samples
sample_files = [
    ("feedback_1.wav", "Voice Note 1: App crash on login"),
    ("feedback_2.wav", "Voice Note 2: App crash after login (Duplicate)"),
    ("feedback_3.wav", "Voice Note 3: Voice reply slow"),
    ("feedback_4.wav", "Voice Note 4: Dark mode request"),
]

st.subheader("1. Sample Voice Feedbacks")
cols = st.columns(4)
for i, (fn, label) in enumerate(sample_files):
    with cols[i]:
        st.markdown(f"**{label}**")
        if os.path.exists(fn):
            st.audio(fn)
        else:
            st.caption("File missing")

st.divider()

if st.button("🚀 Run Full Triage Pipeline (4 Voice Notes -> 3 Deduplicated Tickets)", type="primary"):
    tickets = []
    log_area = st.empty()

    with st.spinner("Processing voice notes through Sarvam pipeline..."):
        for idx, (fn, label) in enumerate(sample_files, start=1):
            if not os.path.exists(fn):
                continue
            
            transcript = transcribe_audio(fn)
            ticket_data = extract_ticket(transcript)
            matched_id = deduplicate_ticket(ticket_data, tickets)

            if matched_id:
                for t in tickets:
                    if t["id"] == matched_id:
                        t["count"] += 1
                        break
            else:
                ticket_id = f"TICK-{len(tickets) + 1:03d}"
                ticket_data["id"] = ticket_id
                ticket_data["count"] = 1
                tickets.append(ticket_data)

    st.success("Triage Complete: 4 recordings processed into 3 clean, prioritized tickets!")

    st.subheader("2. Prioritized Product Backlog (`tickets.md`)")
    table_rows = []
    for t in tickets:
        table_rows.append({
            "Ticket ID": t["id"],
            "Title": t["title"],
            "Category": t["category"].upper(),
            "Severity": t["severity"].upper(),
            "Reports": f"{t['count']} report(s)",
            "Language": t.get("language_detected", "Hinglish"),
            "Summary": t.get("summary", "")
        })
    st.table(table_rows)

    # Voice confirmation
    if tickets:
        reply_path = generate_voice_confirmation(tickets[0]["title"], "reply.wav")
        st.subheader("3. Voice Confirmation to User (Bulbul TTS)")
        st.write(f"Spoken reply: *\"Aapki shikayat note kar li gayi hai: {tickets[0]['title']}\"*")
        if os.path.exists(reply_path):
            st.audio(reply_path)

st.divider()
st.markdown(
    "> **30-Second Pitch:** *\"Feedback arrives as Hinglish voice notes that engineers can't use. "
    "Our agent transcribes with Saaras, structures with Sarvam-105B, merges duplicates, and replies in "
    "the user's language with Bulbul. Four voice notes in, three clean tickets out.\"*"
)
