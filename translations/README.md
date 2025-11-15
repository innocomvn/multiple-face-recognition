# Internationalization (i18n) for FRAMS

This directory contains translation files for FRAMS in multiple languages.

## Supported Languages

- **en** - English (default)
- **vi** - Vietnamese

## Quick Start

### Using i18n in Python Code

```python
from i18n_config import get_text, set_language

# Set language to Vietnamese
set_language('vi')

# Get translated text
welcome_msg = get_text('welcome')  # Returns: "Chào mừng đến với FRAMS"
```

### Using i18n in Flask Templates

```html
<!-- Jinja2 templates automatically have access to translation functions -->
<h1>{{ _('welcome') }}</h1>
<button>{{ _('mark_attendance') }}</button>
<p>{{ get_text('customer_recognized') }}</p>
```

### Using i18n in API Responses

```python
from i18n_config import get_text

@app.route('/api/example')
def example():
    # Language can be determined from request headers
    return jsonify({
        'message': get_text('success'),
        'data': {...}
    })
```

## Adding New Languages

To add support for a new language:

1. **Update `i18n_config.py`:**

   Add a new language dictionary:
   ```python
   TRANSLATIONS = {
       'en': {...},
       'vi': {...},
       'fr': {  # New French translations
           'welcome': 'Bienvenue à FRAMS',
           'success': 'Succès',
           # ... other translations
       }
   }
   ```

2. **Create translation directory:**
   ```bash
   mkdir -p translations/fr/LC_MESSAGES
   ```

3. **Test the translations:**
   ```python
   from i18n_config import set_language, get_text

   set_language('fr')
   print(get_text('welcome'))  # Should print: Bienvenue à FRAMS
   ```

## Adding New Translation Keys

To add a new translatable string:

1. Add the key to all language dictionaries in `i18n_config.py`:
   ```python
   TRANSLATIONS = {
       'en': {
           # ... existing keys
           'new_feature': 'New Feature'
       },
       'vi': {
           # ... existing keys
           'new_feature': 'Tính năng mới'
       }
   }
   ```

2. Use in code:
   ```python
   text = get_text('new_feature')
   ```

## Language Detection

The system automatically detects language in the following order:

1. **Session language** - Set via `session['language']`
2. **Accept-Language header** - From browser/client
3. **Default language** - Falls back to English ('en')

## Setting Language Dynamically

### In Flask Routes

```python
from flask import session
from i18n_config import set_language

@app.route('/set-language/<lang>')
def set_user_language(lang):
    session['language'] = lang
    set_language(lang)
    return jsonify({'success': True, 'language': lang})
```

### In Frontend

```javascript
// Set language via API
fetch('/set-language/vi')
  .then(response => response.json())
  .then(data => {
    console.log('Language changed to:', data.language);
    // Reload page or update UI
    location.reload();
  });
```

## Translation File Structure

```
translations/
├── README.md           # This file
├── en/                 # English translations
│   └── LC_MESSAGES/
├── vi/                 # Vietnamese translations
│   └── LC_MESSAGES/
└── [lang]/            # Additional languages
    └── LC_MESSAGES/
```

## Best Practices

1. **Always use translation keys:**
   ```python
   # Good
   message = get_text('welcome')

   # Bad
   message = "Welcome to FRAMS"
   ```

2. **Keep keys descriptive:**
   ```python
   # Good
   'employee_registered_successfully'

   # Bad
   'msg1'
   ```

3. **Group related keys:**
   ```python
   'employee_name'
   'employee_email'
   'employee_registered'
   ```

4. **Provide context in comments:**
   ```python
   # User greeting message shown on login
   'welcome': 'Welcome to FRAMS'
   ```

## Using with Flask-Babel (Advanced)

For production systems, consider using Flask-Babel for more advanced features:

```bash
# Install Flask-Babel
pip install Flask-Babel

# Initialize babel
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l vi
pybabel compile -d translations
```

## Common Translation Keys

### Actions
- `save`, `cancel`, `delete`, `edit`, `add`
- `search`, `filter`, `export`, `import`
- `upload`, `download`, `refresh`, `close`

### Status Messages
- `success`, `error`, `loading`, `processing`
- `no_results`, `invalid_image`, `required_field`

### Navigation
- `home`, `dashboard`, `reports`, `settings`
- `login`, `logout`, `back`, `next`, `previous`

### Domain-Specific
- `attendance`, `employee`, `customer`
- `mark_attendance`, `register_employee`
- `customer_visit`, `visit_count`

## Testing Translations

```python
# Test all translations for a language
from i18n_config import get_all_translations

translations = get_all_translations('vi')
print(f"Total keys: {len(translations)}")

# Verify all keys have translations
en_keys = set(get_all_translations('en').keys())
vi_keys = set(get_all_translations('vi').keys())
missing = en_keys - vi_keys
if missing:
    print(f"Missing Vietnamese translations: {missing}")
```

## Contributing Translations

We welcome translation contributions! Please:

1. Fork the repository
2. Add/update translations in `i18n_config.py`
3. Test your translations
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## Resources

- [Flask-Babel Documentation](https://flask-babel.tkte.ch/)
- [Python gettext](https://docs.python.org/3/library/gettext.html)
- [ISO 639-1 Language Codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

---

**Last Updated:** 2025-01-15
