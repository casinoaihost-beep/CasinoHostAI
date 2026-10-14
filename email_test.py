import streamlit as st

from notifications import (
    send_test_email,
)


st.title("Casino Host AI - Email Test")

st.write(
    "Klikni gumb ispod za slanje testnog emaila."
)

if st.button("POŠALJI TEST EMAIL"):

    result = send_test_email()

    if result["success"]:

        st.success(
            "Email je uspješno poslan."
        )

    else:

        st.error(
            result["error"]
        )