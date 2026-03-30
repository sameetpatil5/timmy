import streamlit as st

def show_footer(verbose=False):
    # Footer
    st.write("---")

    st.markdown(
        f"""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
{"<p>💡 <strong>Quality Guarantee:</strong> No compression • No resizing • Original preserved</p>" if verbose else ""}
<p>Created with ❤️ for restoring your precious memories</p>
</div>
""",
        unsafe_allow_html=True,
    )

