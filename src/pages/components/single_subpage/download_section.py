import streamlit as st

# def render_download_section(image):
#     # Download section
#     st.subheader("6️⃣ Download Fixed Image")

#     pressed_download = st.download_button(
#         label="⬇️ Download Fixed Image",
#         data=st.session_state.processed_image,
#         file_name=st.session_state.output_filename,
#         mime=f"image/{image.format.lower() if image.format else 'jpeg'}",
#         type="primary",
#         width='stretch',
#         disabled=not st.session_state.processed_image
#     )

#     if not pressed_download:
#         st.success("✅ Your image is ready! Click the button above to download.")

#     else:
#         st.info("👆 Apply changes first, then download the fixed image.")


def render_download_section(image):
    st.subheader("6️⃣ Download Fixed Image")

    if st.session_state.get("processed_image") is not None:

        pressed_download = st.download_button(
            label="⬇️ Download Fixed Image",
            data=st.session_state.processed_image,
            file_name=st.session_state.output_filename,
            mime=f"image/{image.format.lower() if image.format else 'jpeg'}",
            type="primary",
            width="stretch",
        )

        if pressed_download:
            st.success("✅ Download started!")
        else:
            st.success("✅ Your image is ready! Click the button above to download.")

    else:
        st.button(
            label="⬇️ Download Fixed Image",
            type="primary",
            width="stretch",
            disabled=st.session_state.get("processed_image") is None,
        )

        st.info("👈 Apply changes first, then download the fixed image.")
