import streamlit as st
from datetime import datetime


def render_customize_individual_section(batch):
    st.subheader("Customize Individual Images")

    with st.expander("🔧 Advanced: Customize Each Image", expanded=False):

        for i, item in enumerate(batch.items):
            if item.image is None:
                continue

            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 1, 2])

                with col1:
                    st.write(f"**{item.filename}**")

                with col2:
                    st.image(item.image, width=200)

                with col3:
                    current_action = st.selectbox(
                        f"Action",
                        ["keep", "filename", "manual"],
                        index=["keep", "filename", "manual"].index(item.action),
                        key=f"action_{i}",
                        label_visibility="collapsed",
                    )
                    item.action = current_action

                with col4:
                    if current_action == "manual":
                        manual_dt = st.text_input(
                            "Date (YYYY-MM-DD HH:MM:SS)",
                            value=(
                                item.manual_datetime.strftime("%Y-%m-%d %H:%M:%S")
                                if item.manual_datetime
                                else ""
                            ),
                            key=f"manual_{i}",
                            label_visibility="collapsed",
                            placeholder="YYYY-MM-DD HH:MM:SS",
                        )
                        try:
                            item.manual_datetime = datetime.strptime(
                                manual_dt, "%Y-%m-%d %H:%M:%S"
                            )
                        except:
                            st.error("Invalid format")
                    else:
                        target = item.get_target_datetime()
                        if target:
                            st.write(f"→ {target.strftime('%Y-%m-%d %H:%M:%S')}")
                        else:
                            st.write("→ N/A")

                st.divider()
