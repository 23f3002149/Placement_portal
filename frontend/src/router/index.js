import { createRouter, createWebHistory } from "vue-router";






// Login related imports
import login from "../views/login.vue";//“Login naam ka variable banao, aur usme ye file load karo”

//Registration related imports
import company_registration from "../views/company/company_registration.vue";
import Student_registration from "../views/student/Student_registration.vue";


// Admin related imports
import admin_dashboard_layout from "../components/layouts/admin_dashboard_layout.vue";
import admin_dashboard from "../views/admin/admin_dashboard.vue";
import admin_companies from "../views/admin/admin_companies.vue";
import admin_students from "../views/admin/admin_students.vue";
import admin_drives from "../views/admin/admin_placements_drives.vue";
import admin_report from "../views/admin/admin_report.vue";







// company related imports
import company_dashboard_layout from "../components/layouts/company_dashboard_layout.vue";
import company_dashboard from "../views/company/company_dashboard.vue"; 
import company_profile from "../views/company/company_profile.vue";
import company_drives from "../views/company/company_newdrives.vue";
import company_applications from "../views/company/company_applications.vue";







// student related imports
import student_dashboard_layout from "../components/layouts/student_dashboard_layout.vue";
import student_dashboard from "../views/student/student_dashboard.vue";
import student_profile from "../views/student/student_profile.vue";
import drives from "../views/student/student_drive.vue";
import applications from "../views/student/student_application.vue";
import change_password from "../views/student/change_password.vue";

const routes = [
  {
    path: "/",
    component: login
  },

  {
    path: "/register/company",
    component: company_registration,
    // meta: { requiresAuth: true, role: "company" } // Only company can access this route
  },
  {
    path: "/register/student",
    component: Student_registration,
    // meta: { requiresAuth: true, role: "student" } // Only students can access this route
  },

  //student_dashboard
  {
    path: "/student",
    component: student_dashboard_layout,
    children: [
      { path: "", redirect: "dashboard" }, // Default to dashboard
      { path: "dashboard", component:student_dashboard},
      {path:"drives",component:drives  },
      {path:"applications",component:applications },
      {path: "profile", component: student_profile },
      {path: "change-password", component: change_password }
    ]
  },

  //company_dashboard
  {
  path:"/company",
  component:company_dashboard_layout,
  children:[
    {path:"",redirect:"dashboard"},
    {path:"dashboard",component:company_dashboard},
    {path:"drives",component:company_drives},
    {path:"profile",component:company_profile},
    {path:"applications",component:company_applications},
    {path:"change-password",component:change_password}
    ]
  },





  // Admin dashboard
  {
    path: "/admin",
    component:admin_dashboard_layout,
    children:[
      {path:"",redirect:"dashboard"},
      {path:"dashboard",component:admin_dashboard},
      {path:"companies",component:admin_companies},
      {path:"students",component:admin_students},
      {path:"drives",component:admin_drives},
      {path:"report",component:admin_report}
    ]

  }
];
const router = createRouter({//ye bhai humhe router system bananta hai 
// Internally:
// Routes store karta hai
// URL change listen karta hai
// Match karta hai route
// Component render karata hai
  history: createWebHistory(),//ye bhai humhe clean Url detta hai //yahi hai voYe browser ke URL changes ko listen karta hai
  routes
});



//  Route Guard - Frontend pe unauthorized access rokna
router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role"); // ← yaha se lo, pehle define hi nahi tha!

  if (to.meta.requiresAuth && !token) {
    next("/"); // token nahi hai → login page
  }
  else if (to.meta.role && to.meta.role !== role) {
    next("/"); // wrong role → login page
  }
  else {
    next(); // sab theek hai → allow
  }

});





export default router;
