import { BASE_API_URL, BASE_URL } from "../../../../frontend/src/route";

const API_URL = `${BASE_API_URL}/product`;
const PRODUCT_ATTRIBUTE_API_URL = `${BASE_API_URL}/product-attributes`;
const PAGE_URL = `${BASE_URL}/product`;

//! Brand URL =====================================
export const BrandApiURL = {
    List: `${PRODUCT_ATTRIBUTE_API_URL}/brand`,
    Create: `${PRODUCT_ATTRIBUTE_API_URL}/brand`,
    Details: `${PRODUCT_ATTRIBUTE_API_URL}/brand`,
    Update: `${PRODUCT_ATTRIBUTE_API_URL}/brand`,
    Delete: `${PRODUCT_ATTRIBUTE_API_URL}/brand`,
};
//! ====================================================
//! Color URL =====================================
export const ColorApiURL = {
    List: `${PRODUCT_ATTRIBUTE_API_URL}/color`,
    Create: `${PRODUCT_ATTRIBUTE_API_URL}/color`,
    Details: `${PRODUCT_ATTRIBUTE_API_URL}/color`,
    Update: `${PRODUCT_ATTRIBUTE_API_URL}/color`,
    Delete: `${PRODUCT_ATTRIBUTE_API_URL}/color`,
};
//! ====================================================


