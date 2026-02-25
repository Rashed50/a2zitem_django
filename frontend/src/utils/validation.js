/**
 * Validation Utility Functions
 * Reusable validation functions for common form fields
 */

// ===================================================================
// ======================= REGULAR EXPRESSIONS ======================
// ===================================================================
export const REGEX = {
    EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    PHONE: /^[+]?[(]?[0-9]{1,4}[)]?[-\s.]?[(]?[0-9]{1,4}[)]?[-\s.]?[0-9]{1,9}$/,
    NAME: /^[a-zA-Z\s'-]+$/,
    ALPHANUMERIC: /^[a-zA-Z0-9]+$/,
    NUMERIC: /^[0-9]+$/,
    NID: /^[0-9]{10,17}$/, // বাংলাদেশী NID 10 বা 17 ডিজিট
    PASSPORT: /^[A-Z0-9]{6,9}$/, // পাসপোর্ট নম্বর ফরম্যাট
    EMPLOYEE_ID: /^[a-zA-Z0-9_-]{3,20}$/, // Employee ID ফরম্যাট
    URL: /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/,
    DATE: /^\d{4}-\d{2}-\d{2}$/, // YYYY-MM-DD ফরম্যাট
};

// ===================================================================
// ======================== ERROR MESSAGES ==========================
// ===================================================================
export const ERROR_MESSAGES = {
    REQUIRED: (field) => `${field} is required`,
    MIN_LENGTH: (field, min) => `${field} must be at least ${min} characters`,
    MAX_LENGTH: (field, max) => `${field} must be at most ${max} characters`,
    EXACT_LENGTH: (field, length) => `${field} must be exactly ${length} characters`,
    INVALID_FORMAT: (field) => `Invalid ${field} format`,
    INVALID_EMAIL: 'Invalid email format',
    INVALID_PHONE: 'Invalid phone number format',
    INVALID_NAME: 'Name can only contain letters, spaces, and hyphens',
    INVALID_NID: 'NID must be 10 or 17 digits',
    INVALID_PASSPORT: 'Invalid passport number format',
    INVALID_DATE: 'Invalid date format',
    AGE_RESTRICTION: (age) => `You must be at least ${age} years old`,
    FUTURE_DATE: (field) => `${field} cannot be in the future`,
    PAST_DATE: (field) => `${field} cannot be in the past`,
    INVALID_SELECTION: (field) => `Please select a valid ${field}`,

    PASSWORD_REQUIRED: 'Password is required',
    PASSWORD_MIN_LENGTH: (min) => `Password must be at least ${min} characters long`,
    PASSWORD_MAX_LENGTH: (max) => `Password must be at most ${max} characters long`,
    PASSWORD_UPPERCASE: 'Password must contain at least one uppercase letter',
    PASSWORD_LOWERCASE: 'Password must contain at least one lowercase letter',
    PASSWORD_NUMBER: 'Password must contain at least one number',
    PASSWORD_SPECIAL: 'Password must contain at least one special character (!@#$%^&* etc.)',
    PASSWORD_WEAK: (level) => `Password is too weak (${level}). Please choose a stronger password.`,
    PASSWORD_MISMATCH: 'Passwords do not match',
    CONFIRM_PASSWORD_REQUIRED: 'Please confirm your password',
    WEAK_PASSWORD: 'Password must contain at least 8 characters, one uppercase, one lowercase, one number and one special character',
};

// ===================================================================
// ======================== VALIDATION FUNCTIONS ====================
// ===================================================================

/**
 * Check if a value is empty (null, undefined, empty string, or empty array)
 * @param {any} value - The value to check
 * @returns {boolean} - True if empty, false otherwise
 */
export const isEmpty = (value) => {
    return (
        value === null ||
        value === undefined ||
        value === '' ||
        (Array.isArray(value) && value.length === 0) ||
        (typeof value === 'object' && !Array.isArray(value) && Object.keys(value).length === 0)
    );
};

/**
 * Validate required field
 * @param {any} value - The value to validate
 * @param {string} fieldName - Name of the field for error message
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateRequired = (value, fieldName) => {
    if (isEmpty(value)) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.REQUIRED(fieldName)
        };
    }
    return { isValid: true, error: '' };
};

/**
 * Validate minimum length
 * @param {string} value - The string to validate
 * @param {number} min - Minimum length
 * @param {string} fieldName - Name of the field for error message
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateMinLength = (value, min, fieldName) => {
    if (!isEmpty(value) && value.length < min) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.MIN_LENGTH(fieldName, min)
        };
    }
    return { isValid: true, error: '' };
};

/**
 * Validate maximum length
 * @param {string} value - The string to validate
 * @param {number} max - Maximum length
 * @param {string} fieldName - Name of the field for error message
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateMaxLength = (value, max, fieldName) => {
    if (!isEmpty(value) && value.length > max) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.MAX_LENGTH(fieldName, max)
        };
    }
    return { isValid: true, error: '' };
};

/**
 * Validate exact length
 * @param {string} value - The string to validate
 * @param {number} length - Exact length
 * @param {string} fieldName - Name of the field for error message
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateExactLength = (value, length, fieldName) => {
    if (!isEmpty(value) && value.length !== length) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.EXACT_LENGTH(fieldName, length)
        };
    }
    return { isValid: true, error: '' };
};

/**
 * Validate name
 * @param {string} name - The name to validate
 * @param {string} fieldName - Name of the field (e.g., 'First name')
 * @param {Object} options - Additional options { minLength, maxLength, required }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateName = (name, fieldName = 'Name', options = {}) => {
    const { minLength = 2, maxLength = 50, required = true } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(name, fieldName);
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(name)) {
        return { isValid: true, error: '' };
    }

    // Check minimum length
    const minCheck = validateMinLength(name, minLength, fieldName);
    if (!minCheck.isValid) return minCheck;

    // Check maximum length
    const maxCheck = validateMaxLength(name, maxLength, fieldName);
    if (!maxCheck.isValid) return maxCheck;

    // Check format (letters, spaces, hyphens, apostrophes only)
    // if (!REGEX.NAME.test(name)) {
    //     return {
    //         isValid: false,
    //         error: ERROR_MESSAGES.INVALID_NAME
    //     };
    // }

    return { isValid: true, error: '' };
};

/**
 * Validate email
 * @param {string} email - The email to validate
 * @param {Object} options - Additional options { required }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateEmail = (email, options = {}) => {
    const { required = true } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(email, 'Email');
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(email)) {
        return { isValid: true, error: '' };
    }

    // Check email format
    if (!REGEX.EMAIL.test(email)) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.INVALID_EMAIL
        };
    }

    return { isValid: true, error: '' };
};

/**
 * Validate phone number
 * @param {string} phone - The phone number to validate
 * @param {Object} options - Additional options { required, minLength, maxLength }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validatePhone = (phone, options = {}) => {
    const { required = true, minLength = 7, maxLength = 20 } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(phone, 'Phone');
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(phone)) {
        return { isValid: true, error: '' };
    }

    // Check minimum length
    const minCheck = validateMinLength(phone, minLength, 'Phone number');
    if (!minCheck.isValid) return minCheck;

    // Check maximum length
    const maxCheck = validateMaxLength(phone, maxLength, 'Phone number');
    if (!maxCheck.isValid) return maxCheck;

    // Check phone format (basic validation)
    if (!REGEX.PHONE.test(phone)) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.INVALID_PHONE
        };
    }

    return { isValid: true, error: '' };
};

/**
 * Validate password
 * @param {string} password - The password to validate
 * @param {Object} options - Additional options { 
 *    required, 
 *    minLength, 
 *    maxLength,
 *    requireUppercase,
 *    requireLowercase,
 *    requireNumbers,
 *    requireSpecialChars,
 *    minStrengthScore (0-4)
 * }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validatePassword = (password, options = {}) => {
    const {
        required = true,
        minLength = 8,
        maxLength = 32,
        requireUppercase = true,
        requireLowercase = true,
        requireNumbers = true,
        requireSpecialChars = true,
        minStrengthScore = null // 0-4 (0: খুব দুর্বল, 4: খুব শক্তিশালী)
    } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(password, 'Password');
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(password)) {
        return { isValid: true, error: '' };
    }

    // Check minimum length
    if (password.length < minLength) {
        return {
            isValid: false,
            error: `Password must be at least ${minLength} characters long`
        };
    }

    // Check maximum length
    if (password.length > maxLength) {
        return {
            isValid: false,
            error: `Password must be at most ${maxLength} characters long`
        };
    }

    // Check for uppercase letters
    if (requireUppercase && !/[A-Z]/.test(password)) {
        return {
            isValid: false,
            error: 'Password must contain at least one uppercase letter'
        };
    }

    // Check for lowercase letters
    if (requireLowercase && !/[a-z]/.test(password)) {
        return {
            isValid: false,
            error: 'Password must contain at least one lowercase letter'
        };
    }

    // Check for numbers
    if (requireNumbers && !/[0-9]/.test(password)) {
        return {
            isValid: false,
            error: 'Password must contain at least one number'
        };
    }

    // Check for special characters
    // if (requireSpecialChars && !/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    //     return {
    //         isValid: false,
    //         error: 'Password must contain at least one special character (!@#$%^&* etc.)'
    //     };
    // }

    // Calculate password strength if minStrengthScore is provided
    if (minStrengthScore !== null) {
        const strengthScore = calculatePasswordStrength(password);
        if (strengthScore < minStrengthScore) {
            const strengthLabels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
            return {
                isValid: false,
                error: `Password is too weak (${strengthLabels[strengthScore]}). Please choose a stronger password.`
            };
        }
    }

    return { isValid: true, error: '' };
};

/**
 * Calculate password strength score (0-4)
 * @param {string} password - The password to evaluate
 * @returns {number} - Strength score (0: very weak, 4: very strong)
 */
export const calculatePasswordStrength = (password) => {
    if (!password) return 0;

    let score = 0;

    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;

    // Character variety checks
    if (/[a-z]/.test(password)) score++; // has lowercase
    if (/[A-Z]/.test(password)) score++; // has uppercase
    if (/[0-9]/.test(password)) score++; // has number
    if (/[^a-zA-Z0-9]/.test(password)) score++; // has special char

    // Normalize score to 0-4 range (max possible score with above is 6)
    return Math.min(4, Math.floor(score / 1.5));
};

/**
 * Validate password confirmation
 * @param {string} password - The original password
 * @param {string} confirmPassword - The confirmation password
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validatePasswordConfirmation = (password, confirmPassword) => {
    const isPasswordEmpty = isEmpty(password);
    const isConfirmEmpty = isEmpty(confirmPassword);

    if (isPasswordEmpty && isConfirmEmpty) {
        return { isValid: true, error: '' };
    }

    if (isPasswordEmpty && !isConfirmEmpty) {
        return {
            isValid: false,
            error: 'Password is required'
        };
    }

    if (!isPasswordEmpty && isConfirmEmpty) {
        return {
            isValid: false,
            error: 'Please confirm your password'
        };
    }

    if (password !== confirmPassword) {
        return {
            isValid: false,
            error: 'Passwords do not match'
        };
    }

    return { isValid: true, error: '' };
};

/**
 * Generate password strength meter information
 * @param {string} password - The password to evaluate
 * @returns {Object} - Strength information with score, label, color, and requirements status
 */
export const getPasswordStrengthInfo = (password) => {
    const strengthScore = calculatePasswordStrength(password);

    const strengthMap = {
        0: { label: 'Very Weak', color: '#dc3545', message: 'Use at least 8 characters' },
        1: { label: 'Weak', color: '#ff6b6b', message: 'Add numbers and mix case' },
        2: { label: 'Fair', color: '#ffd93d', message: 'Add special characters' },
        3: { label: 'Good', color: '#6bcf7f', message: 'Getting stronger' },
        4: { label: 'Strong', color: '#28a745', message: 'Strong password' }
    };

    const requirements = {
        minLength: password.length >= 8,
        hasLowercase: /[a-z]/.test(password),
        hasUppercase: /[A-Z]/.test(password),
        hasNumber: /[0-9]/.test(password),
        hasSpecialChar: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
    };

    return {
        score: strengthScore,
        ...strengthMap[strengthScore],
        requirements,
        isComplete: Object.values(requirements).every(Boolean)
    };
};

/**
 * Validate date of birth (minimum age requirement)
 * @param {string|Date} dob - Date of birth
 * @param {Object} options - Additional options { required, minAge, maxAge }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateDOB = (dob, options = {}) => {
    const { required = true, minAge = 18, maxAge = 100 } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(dob, 'Date of birth');
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(dob)) {
        return { isValid: true, error: '' };
    }

    try {
        const birthDate = new Date(dob);
        const today = new Date();

        // Check if valid date
        if (isNaN(birthDate.getTime())) {
            return {
                isValid: false,
                error: ERROR_MESSAGES.INVALID_DATE
            };
        }

        // Calculate age
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();

        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }

        // Check minimum age
        if (age < minAge) {
            return {
                isValid: false,
                error: ERROR_MESSAGES.AGE_RESTRICTION(minAge)
            };
        }

        // Check maximum age (optional, for sanity check)
        if (age > maxAge) {
            return {
                isValid: false,
                error: `Age cannot be more than ${maxAge} years`
            };
        }

        // Check if birth date is not in the future
        if (birthDate > today) {
            return {
                isValid: false,
                error: ERROR_MESSAGES.FUTURE_DATE('Date of birth')
            };
        }

        return { isValid: true, error: '' };
    } catch (error) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.INVALID_DATE
        };
    }
};

/**
 * Validate NID (National ID)
 * @param {string} nid - NID number
 * @param {Object} options - Additional options { required }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateNID = (nid, options = {}) => {
    const { required = false } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(nid, 'NID');
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(nid)) {
        return { isValid: true, error: '' };
    }

    // Remove any spaces or dashes
    const cleanNID = nid.toString().replace(/[\s-]/g, '');

    // Check if numeric
    if (!REGEX.NUMERIC.test(cleanNID)) {
        return {
            isValid: false,
            error: 'NID must contain only numbers'
        };
    }

    // Check length (Bangladesh NID: 10 or 17 digits)
    if (cleanNID.length !== 10 && cleanNID.length !== 17) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.INVALID_NID
        };
    }

    return { isValid: true, error: '' };
};

/**
 * Validate Passport number
 * @param {string} passport - Passport number
 * @param {Object} options - Additional options { required }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validatePassport = (passport, options = {}) => {
    const { required = false } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(passport, 'Passport number');
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(passport)) {
        return { isValid: true, error: '' };
    }

    // Remove spaces
    const cleanPassport = passport.toString().replace(/\s/g, '').toUpperCase();

    // Check format (alphanumeric, 6-9 characters)
    if (!REGEX.PASSPORT.test(cleanPassport)) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.INVALID_PASSPORT
        };
    }

    return { isValid: true, error: '' };
};

/**
 * Validate Employee ID
 * @param {string} employeeId - Employee ID
 * @param {Object} options - Additional options { required, minLength, maxLength }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateEmployeeId = (employeeId, options = {}) => {
    const { required = true, minLength = 3, maxLength = 20 } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(employeeId, 'Employee ID');
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(employeeId)) {
        return { isValid: true, error: '' };
    }

    // Check minimum length
    const minCheck = validateMinLength(employeeId, minLength, 'Employee ID');
    if (!minCheck.isValid) return minCheck;

    // Check maximum length
    const maxCheck = validateMaxLength(employeeId, maxLength, 'Employee ID');
    if (!maxCheck.isValid) return maxCheck;

    // Check format (alphanumeric, underscore, hyphen)
    if (!REGEX.EMPLOYEE_ID.test(employeeId)) {
        return {
            isValid: false,
            error: 'Employee ID can only contain letters, numbers, underscores, and hyphens'
        };
    }

    return { isValid: true, error: '' };
};

/**
 * Validate date (not in future)
 * @param {string|Date} date - Date to validate
 * @param {string} fieldName - Name of the field
 * @param {Object} options - Additional options { required, allowFuture }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateDate = (date, fieldName = 'Date', options = {}) => {
    const { required = true, allowFuture = false } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(date, fieldName);
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(date)) {
        return { isValid: true, error: '' };
    }

    try {
        const dateObj = new Date(date);
        const today = new Date();

        // Check if valid date
        if (isNaN(dateObj.getTime())) {
            return {
                isValid: false,
                error: ERROR_MESSAGES.INVALID_DATE
            };
        }

        // Check if date is in future (if not allowed)
        if (!allowFuture && dateObj > today) {
            return {
                isValid: false,
                error: ERROR_MESSAGES.FUTURE_DATE(fieldName)
            };
        }

        return { isValid: true, error: '' };
    } catch (error) {
        return {
            isValid: false,
            error: ERROR_MESSAGES.INVALID_DATE
        };
    }
};

/**
 * Validate joining date (can be in past, not in future)
 * @param {string|Date} date - Joining date
 * @param {Object} options - Additional options { required }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateJoiningDate = (date, options = {}) => {
    return validateDate(date, 'Joining date', { ...options, allowFuture: false });
};

/**
 * Validate selection from choices
 * @param {any} value - Selected value
 * @param {Array} choices - Array of available choices
 * @param {string} fieldName - Name of the field
 * @param {Object} options - Additional options { required, valueKey }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateSelection = (value, choices, fieldName = 'Selection', options = {}) => {
    const { required = true, valueKey = null } = options;

    // Check required
    if (required) {
        const requiredCheck = validateRequired(value, fieldName);
        if (!requiredCheck.isValid) return requiredCheck;
    } else if (isEmpty(value)) {
        return { isValid: true, error: '' };
    }

    // Check if value exists in choices
    if (choices && choices.length > 0) {
        const exists = choices.some(choice => {
            if (valueKey) {
                return choice[valueKey] == value;
            }
            return choice == value || choice.value == value || choice.id == value;
        });

        if (!exists) {
            return {
                isValid: false,
                error: ERROR_MESSAGES.INVALID_SELECTION(fieldName)
            };
        }
    }

    return { isValid: true, error: '' };
};

/**
 * Validate role selections (array)
 * @param {Array} roleIds - Array of selected role IDs
 * @param {Array} roleChoices - Available role choices
 * @param {Object} options - Additional options { required }
 * @returns {Object} - { isValid: boolean, error: string }
 */
export const validateRoles = (roleIds, roleChoices, options = {}) => {
    const { required = false } = options;

    // Check required
    if (required && (!roleIds || roleIds.length === 0)) {
        return {
            isValid: false,
            error: 'At least one role must be selected'
        };
    }

    // If no roles selected and not required, it's valid
    if (!roleIds || roleIds.length === 0) {
        return { isValid: true, error: '' };
    }

    // Check if all role IDs are valid
    if (roleChoices && roleChoices.length > 0) {
        const validRoleIds = roleChoices.map(r => r.id || r.value);
        const invalidRoles = roleIds.filter(id => !validRoleIds.includes(id));

        if (invalidRoles.length > 0) {
            return {
                isValid: false,
                error: 'One or more selected roles are invalid'
            };
        }
    }

    return { isValid: true, error: '' };
};

/**
 * Complete form validator - validates multiple fields at once
 * @param {Object} formData - Form data object
 * @param {Object} validationRules - Validation rules for each field
 * @param {Object} formErrors - Errors object to populate
 * @returns {boolean} - True if form is valid, false otherwise
 */
export const validateForm = (formData, validationRules, formErrors = {}) => {
    let isValid = true;

    // Clear existing errors
    Object.keys(formErrors).forEach(key => {
        if (formErrors[key] !== undefined) {
            formErrors[key] = '';
        }
    });

    // Validate each field according to rules
    for (const [field, rules] of Object.entries(validationRules)) {
        if (!rules) continue;

        const value = formData[field];
        let result = { isValid: true, error: '' };

        // Apply validation based on type
        switch (rules.type) {
            case 'name':
                result = validateName(value, rules.label || field, rules.options || {});
                break;
            case 'email':
                result = validateEmail(value, rules.options || {});
                break;
            case 'phone':
                result = validatePhone(value, rules.options || {});
                break;
            case 'password':
                result = validatePassword(value, rules.options || {});
                break;
            case 'confirm_password':
                const passwordFieldName = rules.options?.passwordFieldName || 'password';
                const passwordValue = formData[passwordFieldName];
                result = validatePasswordConfirmation(passwordValue, value);
                break;
            case 'dob':
                result = validateDOB(value, rules.options || {});
                break;
            case 'nid':
                result = validateNID(value, rules.options || {});
                break;
            case 'passport':
                result = validatePassport(value, rules.options || {});
                break;
            case 'employeeId':
                result = validateEmployeeId(value, rules.options || {});
                break;
            case 'joiningDate':
                result = validateJoiningDate(value, rules.options || {});
                break;
            case 'date':
                result = validateDate(value, rules.label || field, rules.options || {});
                break;
            case 'selection':
                result = validateSelection(value, rules.choices || [], rules.label || field, rules.options || {});
                break;
            case 'roles':
                result = validateRoles(value, rules.choices || [], rules.options || {});
                break;
            case 'required':
                result = validateRequired(value, rules.label || field);
                break;
            case 'custom':
                if (rules.validator && typeof rules.validator === 'function') {
                    result = rules.validator(value, formData);
                }
                break;
            default:
                // If no specific type but has required option
                if (rules.required) {
                    result = validateRequired(value, rules.label || field);
                }
        }

        // Update error and validity
        if (!result.isValid) {
            if (formErrors[field] !== undefined) {
                formErrors[field] = result.error;
            }
            isValid = false;
        }
    }

    return isValid;
};

export default {
    REGEX,
    ERROR_MESSAGES,
    isEmpty,
    validateRequired,
    validateMinLength,
    validateMaxLength,
    validateExactLength,
    validateName,
    validateEmail,
    validatePhone,
    validateDOB,
    validateNID,
    validatePassport,
    validateEmployeeId,
    validateDate,
    validateJoiningDate,
    validateSelection,
    validateRoles,
    validateForm,
};