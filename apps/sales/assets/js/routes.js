import { BASE_API_URL, BASE_URL } from "../../../../frontend/src/route";

const API_URL = `${BASE_API_URL}/sales`;
const PAGE_URL = `${BASE_URL}/sales`;

//! Sales URL =====================================
export const SalesPageURL = {
    List: `${PAGE_URL}/`,
    Create: `${PAGE_URL}/create/`,
    Details: `${PAGE_URL}/details`,
    Update: `${PAGE_URL}/update`,
};
export const SalesApiURL = {
    List: `${API_URL}`,
    Create: `${API_URL}`,
    Details: `${API_URL}`,
    Update: `${API_URL}`,
    Delete: `${API_URL}`,
};

export const ProductVariationListApiURL = `${BASE_API_URL}/product/variant/mini-list/`;
//! ====================================================







const PRODUCT_ATTRIBUTE_API_URL = `${BASE_API_URL}/product-attributes`;
//! Product URL =====================================
export const ProductApiURL = {
    List: `${API_URL}`,
    Create: `${API_URL}`,
    Details: `${API_URL}`,
    Update: `${API_URL}`,
    Delete: `${API_URL}`,
}
export const ProductPageURL = {
    List: `${PAGE_URL}`,
    Create: `${PAGE_URL}/create/`,
    Details: `${PAGE_URL}/details`,
    Update: `${PAGE_URL}/update`,
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

