import { BASE_API_URL, BASE_URL } from "../../../../frontend/src/route";

const API_URL = `${BASE_API_URL}/product`;
const PRODUCT_ATTRIBUTE_API_URL = `${BASE_API_URL}/product-attributes`;
const PAGE_URL = `${BASE_URL}/product`;

//! Product Item URL =====================================
export const ProductItemApiURL = {
    List: `${API_URL}/item`,
    Create: `${API_URL}/item`,
    Details: `${API_URL}/item`,
    Update: `${API_URL}/item`,
    Delete: `${API_URL}/item`,
}
export const ProductItemPageURL = {
    List: `${PAGE_URL}/item`,
    Create: `${PAGE_URL}/item`,
    Details: `${PAGE_URL}/item`,
    Update: `${PAGE_URL}/item`,
    Delete: `${PAGE_URL}/item`,
}
//! ====================================================


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

//! Size URL =====================================
export const SizeApiURL = {
    List: `${PRODUCT_ATTRIBUTE_API_URL}/size`,
    Create: `${PRODUCT_ATTRIBUTE_API_URL}/size`,
    Details: `${PRODUCT_ATTRIBUTE_API_URL}/size`,
    Update: `${PRODUCT_ATTRIBUTE_API_URL}/size`,
    Delete: `${PRODUCT_ATTRIBUTE_API_URL}/size`,
};
//! ====================================================

//! Unit URL =====================================
export const UnitApiURL = {
    List: `${PRODUCT_ATTRIBUTE_API_URL}/unit`,
    Create: `${PRODUCT_ATTRIBUTE_API_URL}/unit`,
    Details: `${PRODUCT_ATTRIBUTE_API_URL}/unit`,
    Update: `${PRODUCT_ATTRIBUTE_API_URL}/unit`,
    Delete: `${PRODUCT_ATTRIBUTE_API_URL}/unit`,
};
//! ====================================================

//! Category URL =====================================
export const CategoryApiURL = {
    MiniList : `${PRODUCT_ATTRIBUTE_API_URL}/category/mini-list/`,
    List: `${PRODUCT_ATTRIBUTE_API_URL}/category`,
    Create: `${PRODUCT_ATTRIBUTE_API_URL}/category`,
    Details: `${PRODUCT_ATTRIBUTE_API_URL}/category`,
    Update: `${PRODUCT_ATTRIBUTE_API_URL}/category`,
    Delete: `${PRODUCT_ATTRIBUTE_API_URL}/category`,
};
export const CategoryPageURL = {
    List: `${PAGE_URL}/category`,
    Create: `${PAGE_URL}/category/create/`,
    Details: `${PAGE_URL}/category/details`,
    Update: `${PAGE_URL}/category/update`,
}
//! ====================================================

