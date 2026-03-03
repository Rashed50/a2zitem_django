import { BASE_API_URL, BASE_URL } from "../../../../frontend/src/route";

const API_URL = `${BASE_API_URL}/product`;
const PRODUCT_ATTRIBUTE_API_URL = `${BASE_API_URL}/product-attributes`;
const PAGE_URL = `${BASE_URL}/product`;

//! Brand URL =====================================
//? Shop API URL
export const BrandApiURL = {
    List: `${PRODUCT_ATTRIBUTE_API_URL}/brand`,
    Create: `${PRODUCT_ATTRIBUTE_API_URL}`,
    Details: `${PRODUCT_ATTRIBUTE_API_URL}`,
    Update: `${PRODUCT_ATTRIBUTE_API_URL}`,
    Delete: `${PRODUCT_ATTRIBUTE_API_URL}`,
};
//! ====================================================



