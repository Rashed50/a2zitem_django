/**
 * Truncate text to specified character limit
 * @param {string} text - The text to truncate
 * @param {number} limit - Maximum character limit
 * @param {string} suffix - Suffix to add after truncation (default: '...')
 * @returns {string} - Truncated text
 */
export const truncateText = (text, limit, suffix = '...') => {
    if (!text) return '';
    if (text.length <= limit) return text;
    return text.substring(0, limit) + suffix;
};

/**
 * Check if text needs truncation
 * @param {string} text - The text to check
 * @param {number} limit - Character limit
 * @returns {boolean} - True if text exceeds limit
 */
export const needsTruncation = (text, limit) => {
    if (!text) return false;
    return text.length > limit;
};

/**
 * Get truncated text with full text for tooltip
 * @param {string} text - The text to process
 * @param {number} limit - Character limit
 * @param {string} suffix - Suffix for truncated text
 * @returns {Object} - Object containing truncated text and full text
 */
export const getTruncatedWithFull = (text, limit, suffix = '...') => {
    return {
        truncated: truncateText(text, limit, suffix),
        full: text || '',
        needsTruncation: needsTruncation(text, limit)
    };
};