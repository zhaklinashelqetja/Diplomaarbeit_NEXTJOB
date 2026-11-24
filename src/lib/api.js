import { getLocale } from '$lib/paraglide/runtime.js';

export const API_URL = 'https://nextjob.htl-cloud.com';

export function localizedUrl(url) {
    const result = new URL(url, API_URL);
    result.searchParams.set('lang', getLocale());
    return result.toString();
}

export function localizedField(data, field) {
    return data?.[`${field}_localized`] ?? data?.[field] ?? '';
}
