/**
 * UTC টাইমস্ট্রিংকে লোকাল টাইমে কনভার্ট করে আলাদা আলাদা ডেট এবং টাইম রিটার্ন করে
 * @param {string} utcDateTime - UTC টাইমস্ট্রিং (যেমন: "2026-02-06T14:52:50.548077+06:00")
 * @returns {Object} - date এবং time প্রপার্টি সহ অবজেক্ট
 */
export function formatLocalDateTime(utcDateTime) {
  if (!utcDateTime) {
    return { date: '', time: '' };
  }
  
  try {
    // Create Date object from UTC string
    const dateObj = new Date(utcDateTime);
    
    // Check if date is valid
    if (isNaN(dateObj.getTime())) {
      return { date: '', time: '' };
    }
    
    // Format date (YYYY-MM-DD format)
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    const date = `${year}-${month}-${day}`;
    
    // Format time (HH:MM:SS format)
    const hours = String(dateObj.getHours()).padStart(2, '0');
    const minutes = String(dateObj.getMinutes()).padStart(2, '0');
    const seconds = String(dateObj.getSeconds()).padStart(2, '0');
    const time = `${hours}:${minutes}:${seconds}`;
    
    return { date, time };
    
  } catch (error) {
    console.error('Error formatting date:', error);
    return { date: '', time: '' };
  }
}

/**
 * বিকল্প: আরো কাস্টমাইজড ফরম্যাটের জন্য
 * @param {string} utcDateTime - UTC টাইমস্ট্রিং
 * @returns {Object} - বিভিন্ন ফরম্যাটে ডেট এবং টাইম
 */
export function formatLocalDateTimeExtended(utcDateTime) {
  if (!utcDateTime) {
    return { 
      date: '', 
      time: '',
      formattedDate: '',
      formattedTime: '',
      fullDateTime: ''
    };
  }
  
  try {
    const dateObj = new Date(utcDateTime);
    
    if (isNaN(dateObj.getTime())) {
      return { 
        date: '', 
        time: '',
        formattedDate: '',
        formattedTime: '',
        fullDateTime: ''
      };
    }
    
    // Basic format
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    const date = `${year}-${month}-${day}`;
    
    // Time with AM/PM
    let hours = dateObj.getHours();
    const minutes = String(dateObj.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 should be 12
    const time = `${String(hours).padStart(2, '0')}:${minutes} ${ampm}`;
    
    // Formatted date (DD/MM/YYYY)
    const formattedDate = `${day}/${month}/${year}`;
    
    // 12-hour format time
    const formattedTime = `${String(hours).padStart(2, '0')}:${minutes} ${ampm}`;
    
    // Full date time string
    const fullDateTime = dateObj.toLocaleString();
    
    return {
      date,              // 2026-02-06
      time,              // 02:52 PM
      formattedDate,     // 06/02/2026
      formattedTime,     // 02:52 PM
      fullDateTime      // 2/6/2026, 2:52:50 PM (depends on locale)
    };
    
  } catch (error) {
    console.error('Error formatting date:', error);
    return { 
      date: '', 
      time: '',
      formattedDate: '',
      formattedTime: '',
      fullDateTime: ''
    };
  }
}

/**
 * শুধুমাত্র সময় রিটার্ন করার জন্য (12-hour format)
 */
export function getLocalTime(utcDateTime) {
  const result = formatLocalDateTimeExtended(utcDateTime);
  return result.formattedTime;
}

/**
 * শুধুমাত্র তারিখ রিটার্ন করার জন্য (DD/MM/YYYY)
 */
export function getLocalDate(utcDateTime) {
  const result = formatLocalDateTimeExtended(utcDateTime);
  return result.formattedDate;
}