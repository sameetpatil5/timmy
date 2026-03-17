# 📸 Image EXIF Date Fixer

A production-ready Streamlit application that restores correct capture dates for images shared via WhatsApp and other platforms that overwrite EXIF metadata.

## 🎯 Problem Solved

When images are shared through WhatsApp:

- **Filename** preserves the original capture date (e.g., `IMG-20241222-WA0135.jpg`)
- **EXIF metadata** gets overwritten with the download date

This app fixes the EXIF DateTimeOriginal while **preserving 100% image quality**.

## ✨ Features

- **Intelligent EXIF Detection:**
  - 🔍 Automatically checks if valid EXIF date exists
  - ✅ Preserves existing EXIF dates by default
  - 🔄 Only uses filename parsing if no EXIF date found
  - ⚙️ Manual override available when needed

- **Three Date Extraction Modes:**
  - 🔹 Automatic filename parsing (WhatsApp, ISO dates, etc.)
  - 🔹 Custom pattern matching with user-defined rules
  - 🔹 Manual date-time entry (can override existing EXIF)

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
   - App automatically checks if valid EXIF date exists

2. **Intelligent Date Handling**
   - **If EXIF date exists:** App preserves it automatically
   - **If no EXIF date:** App extracts from filename or prompts for manual entry
   - **To override existing EXIF:** Use Manual Date-Time Entry mode

3. **Choose Date Extraction Method**
   - **Automatic:** Detects common patterns automatically (used only if no EXIF)
   - **Custom Pattern:** Define your own pattern (used only if no EXIF)
   - **Manual:** Enter date and time directly (overrides existing EXIF)

4. **Select EXIF Fields**
   - Check which datetime fields to update
   - Default: all three selected

5. **Configure Output**
   - Set filename suffix (default: `_fixed`)
   - Preview output filename

6. **Apply & Download**
   - Click "Apply Changes"
   - Review the modification summary
   - See if EXIF was preserved or updated
   - Download the fixed image

## 🧠 How It Works - Smart EXIF Logic

The app uses intelligent logic to determine whether to preserve or update EXIF dates:

### Scenario 1: Image HAS Valid EXIF Date

```bash
✅ Image with existing EXIF: IMG-20241222-WA0135.jpg
   EXIF DateTimeOriginal: 2024-12-22 14:30:15

Result: App preserves "2024-12-22 14:30:15" in output file
Note: Filename date is ignored since reliable EXIF exists
```

### Scenario 2: Image has NO EXIF Date

```bash
⚠️ Image without EXIF: IMG-20241222-WA0135.jpg
   EXIF DateTimeOriginal: (none)

Result: App extracts "2024-12-22" from filename
        Time defaults to 12:00:00
Output: 2024-12-22 12:00:00
```

### Scenario 3: Manual Override

```bash
🔄 User chooses "Manual Date-Time Entry"
   Current EXIF: 2024-12-22 14:30:15
   User sets: 2024-11-15 09:45:00

Result: App updates to user's manual entry
Output: 2024-11-15 09:45:00
```

### Why This Matters

**Problem:** WhatsApp images often have:

- Filename: `IMG-20241222-WA0135.jpg` (original date)
- EXIF: `2025-01-15 10:23:45` (download date) ❌

**Solution:** This app detects the EXIF is newer than expected and uses filename instead.

**Protection:** If EXIF already has the correct original date, it's preserved without changes! ✅

## 📖 Supported Filename Patterns

### Automatic Detection

| Pattern Name           | Example                   | Format         |
| ---------------------- | ------------------------- | -------------- |
| WhatsApp IMG Format    | `IMG-20241222-WA0135.jpg` | `IMG-YYYYMMDD` |
| ISO Date (Hyphens)     | `2024-12-22-photo.jpg`    | `YYYY-MM-DD`   |
| ISO Date (Underscores) | `2024_12_22_photo.jpg`    | `YYYY_MM_DD`   |
| Compact Date           | `20241222_photo.jpg`      | `YYYYMMDD`     |
| Date DDMMYYYY          | `22122024_photo.jpg`      | `DDMMYYYY`     |

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
- `has_valid_exif_datetime()`: Check if valid EXIF date exists (NEW)
- `parse_exif_datetime()`: Parse EXIF datetime strings

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

- **Images with Existing EXIF:** The app automatically preserves valid EXIF dates - no action needed!
- **WhatsApp Images:** If EXIF is corrupted/missing, automatic mode extracts from filename
- **Override Required?** Use Manual Entry mode to force a specific date
- **Ambiguous Dates:** Always verify dates like 01/02/2024
- **Batch Processing:** Upload one at a time for now
- **Quality:** Always download the fixed version, don't overwrite manually

## ❓ FAQ

**Q: Why isn't the filename date being used?**  
A: The image likely has valid EXIF data already. The app preserves existing EXIF to prevent accidental overwrites. Use Manual Entry to override.

**Q: How do I force the app to use the filename date?**  
A: If the image has EXIF but you want to use the filename, switch to Manual Entry mode and input the date from the filename.

**Q: What if both EXIF and filename have wrong dates?**  
A: Use Manual Date-Time Entry to set the correct date.

**Q: Does the app change the original file?**  
A: No! It always creates a new file with `_fixed` suffix. Your original is safe.

## 📧 Support

For issues or questions:

- Open an issue on GitHub
- Check the troubleshooting section
- Review the module documentation

---

**Built with ❤️ for preserving your precious memories**
