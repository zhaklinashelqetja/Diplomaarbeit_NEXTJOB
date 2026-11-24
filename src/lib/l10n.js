import { getLocale } from '$lib/paraglide/runtime.js';

export function getRegionalLocale() {
    const locales = {
        de: 'de-AT',
        sq: 'sq-AL',
        en: 'en-GB'
    };

    return locales[getLocale()] ?? 'de-AT';
}

export function formatDate(value, options = {}) {
    if (!value) return '';

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) return '';

    return new Intl.DateTimeFormat(
        getRegionalLocale(),
        options
    ).format(date);
}

export function formatNumber(value, options = {}) {
    if (value == null || value === '') return '';

    return new Intl.NumberFormat(
        getRegionalLocale(),
        options
    ).format(value);
}

export function formatCurrency(value, currency = 'ALL') {
    return formatNumber(value, {
        style: 'currency',
        currency
    });
}

export function formatRelativeTime(value, unit) {
    return new Intl.RelativeTimeFormat(
        getRegionalLocale(),
        { numeric: 'auto' }
    ).format(value, unit);
}
