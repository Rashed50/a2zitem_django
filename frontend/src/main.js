import { createApp } from 'vue'
import './style.css'

import Swal from 'sweetalert2'
import axios from './plugins/axios'; 
import { ToastifyPlugin } from './plugins/toastify.js';

const app = createApp({});



//! 👉 Import plugins
import { InputeComponentPlugin } from './plugins/inpute.js';
InputeComponentPlugin(app);

import { TextAreaComponentPlugin } from './plugins/textarea.js';
TextAreaComponentPlugin(app);

import { FileInputeComponentPlugin } from './plugins/fileInput.js';
FileInputeComponentPlugin(app);

import { MultiselectComponentPlugin } from './plugins/multiselect.js';
MultiselectComponentPlugin(app);

import { CustomMultiSelectComponentPlugin } from './plugins/customSelect.js';
CustomMultiSelectComponentPlugin(app);

import { DjangoStyleMultiselectPlugin } from './plugins/djangoMultiselect.js';
DjangoStyleMultiselectPlugin(app);

//? Button Components Global Register
import Button from './components/button/Button.vue';
import ActionButton from './components/button/ActionButton.vue';
app.component('Button', Button);
app.component('ActionButton', ActionButton); 

//? Badges Components Global Register
import Badge from './components/badges/Badge.vue';  
import ActionBadge from './components/badges/ActionBadge.vue';
app.component('Badge', Badge);
app.component('ActionBadge', ActionBadge);

//? Card Component Global Register
import InfoCard from './components/card/InfoCard.vue';
app.component('InfoCard', InfoCard);
import MasterCardLayout from './components/card/MasterCardLayout.vue';
app.component('MasterCardLayout', MasterCardLayout);
import MainContentCard from './components/card/MainContentCard.vue';
app.component('MainContentCard', MainContentCard);

//? Checkbox
import Checkbox from './components/inpute/CheckboxComponent.vue';
import CheckboxGroup from './components/inpute/CheckboxGroup.vue';
import SwitchComponent from './components/inpute/SwitchComponent.vue';
import MultipleCheckboxGroup from './components/inpute/MultipleCheckboxGroup.vue';
app.component('Checkbox', Checkbox);
app.component('CheckboxGroup', CheckboxGroup);
app.component('SwitchComponent', SwitchComponent);
app.component('MultipleCheckboxGroup', MultipleCheckboxGroup);


//? Axios set for Global property
app.provide('axios', axios);                    // Composition API এর জন্য
app.config.globalProperties.$axios = axios;     // Options API এর জন্য

//? SweetAlert Global property
app.provide('swal', Swal)                    
app.config.globalProperties.$swal = Swal

//? Toastify Plugin Global property
app.use(ToastifyPlugin);



//! 👉 Import [Template] components -----------------------------------------------------------
//? 👉 Components
import {
    FormComponent,
    ButtonTestComponent,
    BadgesTestComponent,
    TableTestComponent,
} from '../../apps/components/assets/js/app';
app.component("form-test-component", FormComponent);
app.component("button-test-component", ButtonTestComponent);
app.component("badges-test-component", BadgesTestComponent);
app.component("table-test-component", TableTestComponent);

//? 👉 Dashboard Component
import { HomeComponent } from '../../apps/dashboard/assets/js/app';
app.component("dashboard-home-component", HomeComponent);

//! Import Roles-Component
import { 
    RolesListComponent,
    RoleDetailsComponent,
    RoleCreateComponent,
    PermissionsListComponent,
} from '../../apps/roles/assets/js/app';
app.component("roles-list-component", RolesListComponent);
app.component("role-details-component", RoleDetailsComponent);
app.component("role-create-component", RoleCreateComponent);
app.component("permissions-list-component", PermissionsListComponent);


//! Import Supplier Component
import { 
    SupplierCreateUpdateComponent,
    SupplierListComponent,
    SupplierDetailsComponent,
} from '../../apps/supplier/assets/js/app';
app.component("supplier-create-and-update-component", SupplierCreateUpdateComponent);
app.component("supplier-list-component", SupplierListComponent);
app.component("supplier-details-component", SupplierDetailsComponent);

app.mount("#app");