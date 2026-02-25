import { BASE_API_URL, BASE_URL } from "../../../../frontend/src/route";

const API_URL = `${BASE_API_URL}/common`;
const PAGE_URL = `${BASE_URL}/roles`;

export const PermissionApiURL = {
    List: `${API_URL}/permission/`,
}

export const RolePageURL = {
    List: `${PAGE_URL}/`,
    Create: `${PAGE_URL}/create/`,
    Details: `${PAGE_URL}/details`,
    Update: `${PAGE_URL}/update`,
};

export const RoleApiURL = {
    List: `${API_URL}/role/`,
    Details: `${API_URL}/role`,
    Create: `${API_URL}/role/`,
    Update: `${API_URL}/role`,
    Delete: `${API_URL}/role`,
};

//! Employee URL =====================================
//? Employee Page URL
export const EmployeePageURL = {
    List: `${PAGE_URL}/`,
    Create: `${PAGE_URL}/create/`,
    Details: `${PAGE_URL}/details`,
    Update: `${PAGE_URL}/update`,
};

//? Employee API URL
export const EmployeeApiURL = {
    List: `${API_URL}/hr/employee/`,
    Create: `${API_URL}/hr/employee`,
    Details: `${API_URL}/hr/employee`,
    Update: `${API_URL}/hr/employee`,
    Delete: `${API_URL}/hr/employee`,
};
//! ====================================================



