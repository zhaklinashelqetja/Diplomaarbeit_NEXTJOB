import json
from flask import request

SUPPORTED_LOCALES = ("de", "sq", "en")
DEFAULT_LOCALE = "de"


def get_locale():
    locale = request.args.get("lang")

    if locale is None:
        locale = request.headers.get("Accept-Language", DEFAULT_LOCALE)

    locale = locale.split(",")[0].split(";")[0].split("-")[0].lower()

    return locale if locale in SUPPORTED_LOCALES else DEFAULT_LOCALE


def parse_translations(value):
    if isinstance(value, dict):
        return value

    if isinstance(value, (str, bytes)):
        try:
            result = json.loads(value)
            return result if isinstance(result, dict) else {}
        except (ValueError, TypeError):
            return {}

    return {}


def translate_field(original, translations, locale=None):
    locale = locale or get_locale()
    translations = parse_translations(translations)
    if not translations and isinstance(original, str):
        translations = FLAG_REASON_TRANSLATIONS.get(original, {})

    return translations.get(locale) or original


def localize_row(row, fields, locale=None):
    if row is None:
        return None

    locale = locale or get_locale()
    result = dict(row)

    for field in fields:
        translation_key = f"{field}_translations"

        if field in result:
            result[f"{field}_localized"] = translate_field(
                result[field],
                result.get(translation_key),
                locale
            )

        result.pop(translation_key, None)

    return result


def localize_rows(rows, fields, locale=None):
    locale = locale or get_locale()

    return [
        localize_row(row, fields, locale)
        for row in rows
    ]

FLAG_REASON_TRANSLATIONS = {
    "Duplicate text": {
        "de": "Identischer Bewertungstext",
        "sq": "Tekst i përsëritur",
        "en": "Duplicate text"
    },
    "Many reviews same worker": {
        "de": "Viele Bewertungen desselben Dienstleisters",
        "sq": "Shumë vlerësime për të njëjtin punonjës",
        "en": "Many reviews same worker"
    },
    "Review burst": {
        "de": "Viele Bewertungen in kurzer Zeit",
        "sq": "Shumë vlerësime në një kohë të shkurtër",
        "en": "Review burst"
    }
}


def localize_flag_reason(reason, locale=None):
    locale = locale or get_locale()
    return FLAG_REASON_TRANSLATIONS.get(
        reason, {}
    ).get(locale, reason)
