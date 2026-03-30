import streamlit as st

from pages.components.sidebar import show_sidebar
from pages.components.footer import show_footer

show_sidebar()


st.set_page_config(page_title="📚 Tips", page_icon="📚", layout="wide")

st.title("Timmy Tips")
st.write("Some tips and tricks for using Timmy.")

st.markdown(
    """
### 📚 Batch Processing Tips

- **Smart Default**: Best for mixed images (some with EXIF, some without)
- **Filename Mode**: Use when all EXIF dates are wrong/missing
- **Manual Mode**: Use when you know the exact date for all images
- **Individual Customization**: Fine-tune specific images as needed

### 🎯 Example Use Cases

1. **WhatsApp Album**: Upload all images → Use Filename Mode → Process All
2. **Old Photos**: Upload scanned images → Set Manual Date → Process All
3. **Mixed Sources**: Upload images → Use Smart Default → Customize if needed
"""
)

show_footer(verbose=True)
