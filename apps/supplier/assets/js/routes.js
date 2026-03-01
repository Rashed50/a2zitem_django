import { BASE_API_URL, BASE_URL } from "../../../../frontend/src/route";

const API_URL = `${BASE_API_URL}/supplier`;
const PAGE_URL = `${BASE_URL}/supplier`;

//! Supplier URL =====================================
//? Shop Page URL
export const SupplierPageURL = {
    List: `${PAGE_URL}/`,
    Create: `${PAGE_URL}/create/`,
    Details: `${PAGE_URL}/details`,
    Update: `${PAGE_URL}/update`,
};

//? Shop API URL
export const SupplierApiURL = {
    List: `${API_URL}`,
    Create: `${API_URL}`,
    Details: `${API_URL}`,
    Update: `${API_URL}`,
    Delete: `${API_URL}`,
};
//! ====================================================



