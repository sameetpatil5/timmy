# 📸 Image EXIF Date Fixer

A production-ready Streamlit application that restores correct capture dates for images shared via WhatsApp and other platforms that overwrite EXIF metadata.

## 🎯 Problem Solved

When images are shared through WhatsApp:

- **Filename** preserves the original capture date (e.g., `IMG-20241222-WA0135.jpg`)
- **EXIF metadata** gets overwritten with the download date

This app fixes the EXIF DateTimeOriginal while **preserving 100% image quality**.

## ✨ Features

- **Three Date Extraction Modes:**
  - 🔹 Automatic filename parsing (WhatsApp, ISO dates, etc.)
  - 🔹 Custom pattern matching with user-defined rules
  - 🔹 Manual date-time entry

- **Quality Preservation:**
  - ✅ No compression
  - ✅ No resizing
  - ✅ Maintains ICC color profile
  - ✅ Creates new copy (original untouched)

- **Flexible EXIF Control:**
  - Update DateTimeOriginal
  - Update DateTimeDigitized
  - Update DateTime
  - Select any combination

- **Smart Validation:**
  - Ambiguous date warnings (DD/MM vs MM/DD)
  - Future date detection
  - Format validation
  - Quality checks

## 📁 Project Structure

```bash
image-exif-fixer/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── config/
│   └── patterns.py            # Date pattern configurations
│
└── utils/
    ├── image_loader.py        # Image loading & preview
    ├── exif_reader.py         # EXIF metadata reading
    ├── exif_writer.py         # EXIF metadata writing
    ├── filename_parser.py     # Date extraction from filenames
    ├── validators.py          # Input validation
    └── file_exporter.py       # Quality-preserving export
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the project:**

```bash
git clone <repository-url>
cd image-exif-fixer
```

1. **Create virtual environment (recommended):**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Running the App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Step-by-Step Guide

1. **Upload Image**
   - Drag & drop or browse for JPG/PNG files
   - View image preview and current EXIF data

2. **Choose Date Extraction Method**
   - **Automatic:** Detects common patterns automatically
   - **Custom Pattern:** Define your own pattern (e.g., `IMG-{YYYY}{MM}{DD}`)
   - **Manual:** Enter date and time directly

3. **Select EXIF Fields**
   - Check which datetime fields to update
   - Default: all three selected

4. **Configure Output**
   - Set filename suffix (default: `_fixed`)
   - Preview output filename

5. **Apply & Download**
   - Click "Apply Changes"
   - Review the modification summary
   - Download the fixed image

## 📖 Supported Filename Patterns

### Automatic Detection

| Pattern Name | Example | Format |
| ---------------- | --------- | -------- |
| WhatsApp IMG Format | `IMG-20241222-WA0135.jpg` | `IMG-YYYYMMDD` |
| ISO Date (Hyphens) | `2024-12-22-photo.jpg` | `YYYY-MM-DD` |
| ISO Date (Underscores) | `2024_12_22_photo.jpg` | `YYYY_MM_DD` |
| Compact Date | `20241222_photo.jpg` | `YYYYMMDD` |
| Date DDMMYYYY | `22122024_photo.jpg` | `DDMMYYYY` |

### Custom Pattern Placeholders

- `{YYYY}` - 4-digit year (2024)
- `{MM}` - 2-digit month (01-12)
- `{DD}` - 2-digit day (01-31)
- `{HH}` - 2-digit hour (00-23) - optional
- `{mm}` - 2-digit minute (00-59) - optional
- `{SS}` - 2-digit second (00-59) - optional

**Example Custom Pattern:**

```bash
IMG-{YYYY}{MM}{DD}-WA{HH}{mm}
```

Matches: `IMG-20241222-WA1430.jpg` → `2024-12-22 14:30:00`

## 🧪 Testing

### Manual Testing Checklist

- [ ] Upload JPG image
- [ ] Upload PNG image
- [ ] Test automatic parsing with WhatsApp format
- [ ] Test custom pattern matching
- [ ] Test manual date entry
- [ ] Verify EXIF fields are updated
- [ ] Confirm no quality loss
- [ ] Test with image without EXIF
- [ ] Test with corrupted EXIF
- [ ] Test ambiguous date warning

### Quality Validation

The app includes automatic quality checks:

- Output file size monitoring
- Warning if file size decreases >20%
- Maintains original resolution
- Preserves color profile

## 🛡️ Edge Cases Handled

✅ Images without EXIF (creates new EXIF)  
✅ PNG files (limited EXIF support with fallback)  
✅ Filenames without dates (graceful error)  
✅ Ambiguous dates (DD/MM vs MM/DD warning)  
✅ Future dates (validation error)  
✅ Corrupted EXIF blocks (safe handling)  
✅ Unicode filenames (full support)  

## 🔧 Technical Details

### EXIF Fields Modified

- **DateTimeOriginal** (`0x9003`): Original capture time
- **DateTimeDigitized** (`0x9004`): Digitization time
- **DateTime** (`0x0132`): File modification time

### Image Quality Preservation

**JPEG:**

- Quality: 100 (maximum)
- Subsampling: 4:4:4 (no chroma subsampling)
- ICC Profile: Preserved
- No recompression beyond metadata update

**PNG:**

- Compression: Level 9 (lossless)
- EXIF stored as PNG text chunk (Base64)
- Fully lossless format

## 📝 Module Documentation

### `config/patterns.py`

Centralized date pattern configurations with regex definitions.

### `utils/image_loader.py`

- `load_image()`: Load image without modifications
- `get_image_info()`: Extract image metadata
- `validate_image_format()`: Format validation

### `utils/exif_reader.py`

- `read_exif_data()`: Safe EXIF reading
- `get_datetime_original()`: Extract DateTimeOriginal
- `get_all_datetime_fields()`: Extract all datetime fields

### `utils/exif_writer.py`

- `update_exif_datetime()`: Update EXIF fields
- `exif_dict_to_bytes()`: Serialize EXIF data
- `get_modification_summary()`: Generate change summary

### `utils/filename_parser.py`

- `parse_filename_auto()`: Automatic pattern detection
- `parse_filename_custom()`: Custom pattern parsing
- `get_pattern_examples()`: Format pattern help text

### `utils/validators.py`

- `validate_date()`: Date component validation
- `validate_datetime()`: DateTime string validation
- `validate_custom_pattern()`: Pattern syntax validation

### `utils/file_exporter.py`

- `save_image_with_exif()`: Quality-preserving save
- `generate_output_filename()`: Filename generation
- `validate_output_bytes()`: Quality check

## 🐛 Troubleshooting

**Issue:** App doesn't start

```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue:** EXIF not updating

- Ensure at least one checkbox is selected
- Check that the image format supports EXIF (PNG has limitations)
- Try with a JPEG image first

**Issue:** File size warning

- This is normal for PNG files
- For JPEG, verify original quality wasn't already low
- The warning appears if output is >20% smaller

## 🚀 Future Enhancements

- [ ] Batch image processing
- [ ] CSV mapping (filename → date)
- [ ] Undo/history log
- [ ] Dark mode UI
- [ ] Metadata comparison table
- [ ] CLI version
- [ ] GPS coordinate support
- [ ] Camera make/model preservation

## 📄 License

MIT License - Feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 💡 Tips

- **WhatsApp Images:** Use automatic mode for best results
- **Ambiguous Dates:** Always verify dates like 01/02/2024
- **Batch Processing:** Upload one at a time for now
- **Quality:** Always download the fixed version, don't overwrite manually

## 📧 Support

For issues or questions:

- Open an issue on GitHub
- Check the troubleshooting section
- Review the module documentation

---

**Built with ❤️ for preserving your precious memories**
