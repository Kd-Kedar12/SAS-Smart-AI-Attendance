import streamlit as st

import io

try:
    import segno
    SEGNO_AVAILABLE = True
except Exception:
    SEGNO_AVAILABLE = False

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "sasclass-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to Join")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info('Copy this link to share on Whatsapp or Email')

    with col2:
        st.markdown('### Scan to Join')
        if SEGNO_AVAILABLE:
            qr = segno.make(join_url)
            out = io.BytesIO()
            qr.save(out, kind='png', scale=10, border=1)
            st.image(out.getvalue(), caption='QRCODE for class joining')
        else:
            st.warning('QR code generation not available (segno missing). Copy the link to share.')
