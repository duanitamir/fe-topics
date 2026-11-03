"""Small offline SVG icons for the guide's controlled tag vocabulary."""
ICONS = {
    'design-pattern': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 17.5h7m-3.5-3.5v7"/>',
    'react': '<ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/>',
    'browser': '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
    'http': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/>',
    'state-management': '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="19" r="2"/><path d="M7 6h10M6 8l5 9m7-9-5 9"/>',
    'accessibility': '<circle cx="12" cy="4" r="2"/><path d="M4 8l8 2 8-2M12 10v5m0 0-5 6m5-6 5 6"/>',
    'security': '<path d="M12 3l8 3v6c0 5-8 9-8 9s-8-4-8-9V6zM8 12l3 3 5-6"/>',
    'performance': '<path d="M4 19a10 10 0 1 1 16 0M12 13l5-6M5 13H3m18 0h-2M7 6 5 4m7 1V3"/><circle cx="12" cy="13" r="2"/>',
    'concurrency': '<path d="M4 6h16m-4-4 4 4-4 4M20 18H4m4-4-4 4 4 4"/>',
    'resilience': '<path d="M20 8a9 9 0 1 0 1 7M20 3v5h-5M8 12l3 3 5-6"/>',
    'resource-lifecycle': '<path d="M20 7a9 9 0 0 0-15-2L3 7m0-5v5h5M4 17a9 9 0 0 0 15 2l2-2m0 5v-5h-5"/>',
    'api-integration': '<path d="m9 8 6-4a4 4 0 0 1 5 6l-4 3M15 16l-6 4a4 4 0 0 1-5-6l4-3M8 16l8-8"/>',
    'architecture': '<rect x="8" y="2" width="8" height="5" rx="1"/><rect x="2" y="17" width="7" height="5" rx="1"/><rect x="15" y="17" width="7" height="5" rx="1"/><path d="M12 7v5M5.5 17v-5h13v5"/>',
    'forms': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 7h8M8 12h8M8 17h4"/>',
    'rendering': '<path d="m12 3 10 5-10 5L2 8zM2 12l10 5 10-5M2 16l10 5 10-5"/>',
    'storage': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
    'javascript': '<rect x="2" y="2" width="20" height="20" rx="2"/><path d="M10 8v7c0 3-4 3-4 0M18 9c-4-3-6 2-2 3 5 1 2 7-2 4"/>',
    'typescript': '<rect x="2" y="2" width="20" height="20" rx="2"/><path d="M5 8h7m-3.5 0v10M19 9c-4-3-6 2-2 3 5 1 2 7-2 4"/>',
    'graphql': '<path d="m12 2 9 5v10l-9 5-9-5V7zm0 0L3 17h18zm-9 5 9 15 9-15"/>',
    'tooling': '<path d="M14 6a5 5 0 0 0-6 6L3 17a3 3 0 0 0 4 4l5-5a5 5 0 0 0 6-6l-4 3-3-3z"/>',
    'all': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
}
def icon(tag):
    return '<svg class="tag-icon" data-tag-icon="'+tag+'" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+ICONS[tag]+'</svg>'
