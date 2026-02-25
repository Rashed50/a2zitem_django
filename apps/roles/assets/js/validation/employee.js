export const createEmployeeValidationRules = (choices = {}) => {
    return {
        first_name: {
            type: 'name',
            label: 'First name',
            options: { required: true, minLength: 2, maxLength: 50 }
        },
        last_name: {
            type: 'name',
            label: 'Last name',
            options: { required: true, minLength: 2, maxLength: 50 }
        },
        email: {
            type: 'email',
            options: { required: true }
        },
        phone: {
            type: 'phone',
            options: { required: true, minLength: 7, maxLength: 20 }
        },
        gender: {
            type: 'selection',
            label: 'Gender',
            choices: choices.genderChoices || [],
            options: { required: true, valueKey: 'value' }
        },
        dob: {
            type: 'dob',
            options: { required: true, minAge: 18 }
        },
        religion_id: {
            type: 'selection',
            label: 'Religion',
            choices: choices.religionChoices || [],
            options: { required: true, valueKey: 'value' }
        },
        blood_group: {
            type: 'selection',
            label: 'Blood group',
            choices: choices.bloodGroupChoices || [],
            options: { required: false, valueKey: 'value' }
        },
        nid: {
            type: 'nid',
            options: { required: false }
        },
        passport_no: {
            type: 'passport',
            options: { required: false }
        },
        password: {
            type: 'password',
            options: {
                required: false,
                minLength: 8,
                maxLength: 32,
                requireUppercase: true,
                requireLowercase: true,
                requireNumbers: true,
                requireSpecialChars: true,
                minStrengthScore: 2       // পাসওয়ার্ড শক্তির মাত্রা (0-4)
            }
        },
        confirm_password: {
            type: 'confirm_password',
            options: {
                required: false,
                minLength: 8,
                passwordFieldName: 'password' 
            }
        },
        company_id: {
            type: 'selection',
            label: 'Company',
            choices: choices.companyChoices || [],
            options: { required: true, valueKey: 'value' }
        },
        employee_id: {
            type: 'employeeId',
            options: { required: true, minLength: 3, maxLength: 20 }
        },
        joining_date: {
            type: 'joiningDate',
            options: { required: true }
        },
        department_id: {
            type: 'selection',
            label: 'Department',
            choices: choices.departmentChoices || [],
            options: { required: false, valueKey: 'value' }
        },
        designation_id: {
            type: 'selection',
            label: 'Designation',
            choices: choices.designationChoices || [],
            options: { required: false, valueKey: 'value' }
        },
        status: {
            type: 'selection',
            label: 'Status',
            choices: choices.empStatusChoices || [],
            options: { required: true, valueKey: 'value' }
        },
        role_ids: {
            type: 'roles',
            choices: choices.roleChoices || [],
            options: { required: true }
        }
    };
};

export default { createEmployeeValidationRules };






//! Menual Validation
// const validateFormaa = () => {
//    let isValid = true;
//    // Basic required fields
//    const required = [
//       'first_name',
//       'last_name',
//       'email',
//       'phone',
//       'gender',
//       'dob',
//       'religion_id',
//       'employee_id',
//       'joining_date',
//    ];
//    required.forEach((field) => {
//       if (!formData.value[field] && formData.value[field] !== 0) {
//          formErrors[field] = `${field.replace(/_/g, ' ')} is required`;
//          isValid = false;
//       }
//    });

//    // Specific rules
//    if (formData.value.first_name?.trim()?.length < 2) {
//       formErrors.first_name = 'First name must be at least 2 characters';
//       isValid = false;
//    }
//    if (formData.value.last_name?.trim()?.length < 2) {
//       formErrors.last_name = 'Last name must be at least 2 characters';
//       isValid = false;
//    }
//    if (formData.value.email) {
//       const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//       if (!emailRegex.test(formData.value.email)) {
//          formErrors.email = 'Invalid email format';
//          isValid = false;
//       }
//    }
//    if (formData.value.phone?.length < 7 || formData.value.phone?.length > 15) {
//       formErrors.phone = 'Phone number must be between 7 and 15 characters';
//       isValid = false;
//    }
//    // dob validation 18+
//    if (formData.value.dob) {
//       const dob = new Date(formData.value.dob);
//       const today = new Date();
//       const age = today.getFullYear() - dob.getFullYear();
//       if (age < 18) {
//          formErrors.dob = 'You must be at least 18 years old';
//          isValid = false;
//       }
//    }
//    // if (formData.value.religion_id)
//    if (formData.value.employee_id?.length < 3 || formData.value.employee_id?.length > 20) {
//       formErrors.employee_id = 'Employee ID must be between 7 and 15 characters';
//       isValid = false;
//    }
//    // joining_date
//    if (formData.value.joining_date) {
//       const joiningDate = new Date(formData.value.joining_date);
//       const today = new Date();
//       if (joiningDate > today) {
//          formErrors.joining_date = 'Joining date cannot be in the future';
//          isValid = false;
//       }
//    }
//    return isValid;
// };