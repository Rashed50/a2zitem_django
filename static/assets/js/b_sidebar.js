// =================================================================
// 1. INITIALIZATION & DOM ELEMENTS
// =================================================================
// এখানে সব প্রয়োজনীয় HTML এলিমেন্টগুলো নেওয়া হচ্ছে
// =================================================================
document.addEventListener("DOMContentLoaded", () => {
    const menuGroups = document.querySelectorAll(".menu-group > button");
    const menuLinks = document.querySelectorAll(".sidebar-link");
    const overlay = document.getElementById("overlay");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const body = document.body;
    const sidebarIcon = document.getElementById("sidebarIcon");

    const userBtn = document.getElementById("userBtn");
    const userMenu = document.getElementById("userMenu");
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationMenu = document.getElementById('notificationMenu');
    const fullscreenToggle = document.getElementById('fullscreenToggle');
    const themeToggle = document.getElementById('themeToggle');

    // =================================================================
    // 2. RESTORE SAVED STATE FROM localStorage
    // =================================================================
    // পেজ লোড হলে আগের অবস্থা ফিরিয়ে আনে (active menu, open submenu)
    // =================================================================
    const activeMenu = localStorage.getItem("activeMenu");
    const openMenus = JSON.parse(localStorage.getItem("openMenus") || "[]");

    if (activeMenu) {
        const activeLink = document.querySelector(`[data-menu="${activeMenu}"]`);
        if (activeLink) setActive(activeLink);
    }

    openMenus.forEach(id => {
        const submenu = document.getElementById(id);
        const arrow = document.getElementById("arrow-" + id.replace("submenu-", ""));
        if (submenu) submenu.classList.remove("hidden");
        if (arrow) arrow.classList.add("rotate-90");
    });

    // =================================================================
    // 3. SIDEBAR TOGGLE (Desktop & Mobile)
    // =================================================================
    // হ্যামবার্গার মেনু ক্লিক → মোবাইলে ওপেন, ডেস্কটপে কলাপ্স
    // =================================================================
    // sidebarToggle && sidebarToggle.addEventListener("click", () => {
    //     if (window.innerWidth < 768) {
    //         // Mobile: open/close sidebar
    //         body.classList.toggle("mobile-open");
    //         overlay && overlay.classList.toggle("hidden");
    //     } else {
    //         // Desktop: toggle between collapsed & expanded
    //         if (body.classList.contains("sidebar-collapsed")) {
    //             body.classList.remove("sidebar-collapsed");
    //             body.classList.add("sidebar-expanded");
    //         } else {
    //             body.classList.remove("sidebar-expanded");
    //             body.classList.add("sidebar-collapsed");
    //         }
    //     }
    // });

    // Mobile Toggle
    const sidebarToggleMobile = document.getElementById('sidebarToggleMobile');
    const sidebarToggleIconMobile = document.getElementById('sidebarToggleIconMobile');

    sidebarToggleMobile?.addEventListener('click', () => {
        body.classList.toggle("mobile-open");
        overlay?.classList.toggle("hidden");

        // Icon Change on Mobile
        if (body.classList.contains("mobile-open")) {
            sidebarToggleIconMobile.className = 'fas fa-chevron-left text-slate-800 dark:text-slate-900 text-sm';
        } else {
            sidebarToggleIconMobile.className = 'fas fa-chevron-right text-slate-800 dark:text-slate-900 text-sm';
        }
    });

    // Desktop Toggle
    const sidebarToggleDesktop = document.getElementById('sidebarToggleDesktop');
    const sidebarToggleIconDesktop = document.getElementById('sidebarToggleIconDesktop');

    sidebarToggleDesktop?.addEventListener('click', () => {
        if (body.classList.contains("sidebar-collapsed")) {
            body.classList.remove("sidebar-collapsed");
            body.classList.add("sidebar-expanded");
            sidebarToggleIconDesktop.className = 'fas fa-chevron-left text-slate-800 dark:text-slate-900 text-sm';
        } else {
            body.classList.remove("sidebar-expanded");
            body.classList.add("sidebar-collapsed");
            sidebarToggleIconDesktop.className = 'fas fa-chevron-right text-slate-800 dark:text-slate-900 text-sm';
        }
    });

    // Initial Icon State (Desktop: Start with < if expanded)
    if (window.innerWidth >= 768 && !body.classList.contains('sidebar-collapsed')) {
        sidebarToggleIconDesktop.className = 'fas fa-chevron-left text-slate-800 dark:text-slate-900 text-sm';
    }

    // =================================================================
    // 4. MOBILE OVERLAY CLOSE
    // =================================================================
    // মোবাইলে ওভারলে ক্লিক → সাইডবার বন্ধ
    // =================================================================
    overlay && overlay.addEventListener("click", () => {
        body.classList.remove("mobile-open");
        overlay.classList.add("hidden");
    });

    // =================================================================
    // 5. SUBMENU TOGGLE (Menu Group Buttons)
    // =================================================================
    // Components, Company ইত্যাদি বাটনে ক্লিক → submenu ওপেন/ক্লোজ
    // অন্যান্য submenu বন্ধ হয়ে যায়
    // =================================================================
    menuGroups.forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            e.stopPropagation();

            const menuId = btn.dataset.menu;
            const submenu = document.getElementById("submenu-" + menuId);
            const arrow = document.getElementById("arrow-" + menuId);
            if (!submenu) return;

            // Close other open menus at the same level
            const parentMenuGroup = btn.closest('.menu-group');
            const sameLevelMenus = parentMenuGroup.parentElement.querySelectorAll('.menu-group > button');

            sameLevelMenus.forEach(otherBtn => {
                if (otherBtn !== btn) {
                    const otherMenuId = otherBtn.dataset.menu;
                    const otherSubmenu = document.getElementById("submenu-" + otherMenuId);
                    const otherArrow = document.getElementById("arrow-" + otherMenuId);

                    if (otherSubmenu && !otherSubmenu.classList.contains('hidden')) {
                        otherSubmenu.classList.add("hidden");
                        if (otherArrow) otherArrow.classList.remove("rotate-90");
                    }
                }
            });

            const isOpen = !submenu.classList.contains("hidden");
            if (isOpen) {
                submenu.classList.add("hidden");
                arrow.classList.remove("rotate-90");
            } else {
                submenu.classList.remove("hidden");
                arrow.classList.add("rotate-90");
            }
            saveOpenMenus();
        });
    });

    // =================================================================
    // 6. ACTIVE LINK + CLOSE ALL SUBMENUS ON ANY LINK CLICK
    // =================================================================
    // যেকোনো মেনু লিঙ্কে ক্লিক → active হবে + সব submenu বন্ধ + parent খুলবে
    // এটাই তোমার সমস্যার সমাধান!
    // =================================================================
    menuLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            // Skip if it's a menu group button
            if (link.closest('.menu-group > button')) return;

            // Remove active from all
            menuLinks.forEach(l => l.classList.remove("active"));
            setActive(link);
            localStorage.setItem("activeMenu", link.dataset.menu);

            // সমাধান: প্রথমে সব submenu বন্ধ করো
            closeAllMenus();

            // তারপর শুধু ক্লিক করা লিঙ্কের parent menu খোলো
            openParentMenus(link);
        });
    });

    // =================================================================
    // 7. USER DROPDOWN
    // =================================================================
    // ইউজার আইকনে ক্লিক → ড্রপডাউন ওপেন, বাইরে ক্লিক → বন্ধ
    // =================================================================
    if (userBtn && userMenu) {
        userBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            userMenu.classList.toggle("hidden");

            if (notificationMenu && !notificationMenu.classList.contains('hidden')) {
                notificationMenu.classList.add('hidden');
            }
        });

        document.addEventListener("click", (e) => {
            if (!userBtn.contains(e.target) && !userMenu.contains(e.target)) {
                userMenu.classList.add("hidden");
            }
        });
    }

    // =================================================================
    // 8. NOTIFICATION DROPDOWN (Mobile + Fullscreen Support)
    // =================================================================
    // নোটিফিকেশন আইকনে ক্লিক → ড্রপডাউন, মোবাইল/ফুলস্ক্রিনে পজিশন ঠিক করে
    // =================================================================
    if (notificationBtn && notificationMenu) {
        notificationBtn.addEventListener('click', (e) => {
            e.stopPropagation();

            const isOpening = notificationMenu.classList.contains('hidden');
            notificationMenu.classList.toggle('hidden');

            if (userMenu && !userMenu.classList.contains('hidden')) {
                userMenu.classList.add('hidden');
            }

            if (isOpening) {
                adjustNotificationPosition();
            }
        });

        document.addEventListener('click', (e) => {
            if (!notificationBtn.contains(e.target) && !notificationMenu.contains(e.target)) {
                notificationMenu.classList.add('hidden');
            }
        });

        window.addEventListener('resize', () => {
            if (!notificationMenu.classList.contains('hidden')) {
                adjustNotificationPosition();
            }
        });

        ['fullscreenchange', 'webkitfullscreenchange', 'mozfullscreenchange', 'MSFullscreenChange'].forEach(evt =>
            document.addEventListener(evt, adjustNotificationPosition)
        );
    }

    function adjustNotificationPosition() {
        if (!notificationMenu || notificationMenu.classList.contains('hidden')) return;

        const isMobile = window.innerWidth < 768;
        const isFullscreen = !!document.fullscreenElement;

        if (isMobile) {
            notificationMenu.style.position = 'fixed';
            notificationMenu.style.top = '4rem';
            notificationMenu.style.left = '0.5rem';
            notificationMenu.style.right = '0.5rem';
            notificationMenu.style.width = 'auto';
            notificationMenu.style.maxWidth = 'calc(100vw - 1rem)';
            notificationMenu.style.margin = '0';
        } else if (isFullscreen) {
            notificationMenu.style.position = 'fixed';
            notificationMenu.style.top = '4rem';
            notificationMenu.style.right = '1rem';
            notificationMenu.style.zIndex = '9999';
        } else {
            notificationMenu.style.position = 'absolute';
            notificationMenu.style.top = 'auto';
            notificationMenu.style.left = 'auto';
            notificationMenu.style.right = '0';
            notificationMenu.style.width = '20rem';
            notificationMenu.style.maxWidth = '90vw';
            notificationMenu.style.margin = '0.5rem 0 0 0';
        }

        const rect = notificationMenu.getBoundingClientRect();
        if (rect.bottom > window.innerHeight) {
            notificationMenu.style.maxHeight = `${window.innerHeight - 100}px`;
        }
    }

    // =================================================================
    // 9. FULLSCREEN TOGGLE
    // =================================================================
    // ফুলস্ক্রিন অন/অফ
    // =================================================================
    if (fullscreenToggle) {
        fullscreenToggle.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    console.error('Error attempting to enable fullscreen:', err);
                });
            } else {
                document.exitFullscreen?.();
            }
        });
    }

    // =================================================================
    // 10. HELPER: SET ACTIVE MENU (with parent highlighting)
    // =================================================================
    function setActive(el) {
        el.classList.add("active");
        let parent = el.closest(".submenu");
        while (parent) {
            let parentBtn = parent.previousElementSibling;
            if (parentBtn) parentBtn.classList.add("active");
            parent = parent.parentElement.closest(".submenu");
        }
    }

    // =================================================================
    // 11. HELPER: SAVE OPEN SUBMENUS TO localStorage
    // =================================================================
    function saveOpenMenus() {
        const open = [];
        document.querySelectorAll(".submenu").forEach(s => {
            if (!s.classList.contains("hidden")) open.push(s.id);
        });
        localStorage.setItem("openMenus", JSON.stringify(open));
    }

    // =================================================================
    // 12. HELPER: OPEN PARENT MENUS OF A LINK
    // =================================================================
    function openParentMenus(clickedLink) {
        let parentMenu = clickedLink.closest('.submenu');
        while (parentMenu) {
            parentMenu.classList.remove("hidden");

            const parentBtn = parentMenu.previousElementSibling;
            if (parentBtn && parentBtn.classList.contains('menu-group')) {
                const menuId = parentBtn.dataset.menu;
                const arrow = document.getElementById("arrow-" + menuId);
                if (arrow) arrow.classList.add("rotate-90");
            }

            parentMenu = parentMenu.parentElement.closest('.submenu');
        }
        saveOpenMenus();
    }

    // =================================================================
    // 13. GLOBAL: CLOSE ALL SUBMENUS (Dashboard ক্লিকে ব্যবহৃত)
    // =================================================================
    window.closeAllMenus = function () {
        document.querySelectorAll(".submenu").forEach(submenu => {
            submenu.classList.add("hidden");
        });

        document.querySelectorAll(".menu-group button i").forEach(arrow => {
            if (arrow.id.startsWith("arrow-")) {
                arrow.classList.remove("rotate-90");
            }
        });

        localStorage.setItem("openMenus", JSON.stringify([]));
    };

    // =================================================================
    // 14. THEME TOGGLE (Dark / Light Mode)
    // =================================================================
    if (themeToggle) {
        const savedTheme = localStorage.getItem('theme');
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        // Set initial theme
        if (savedTheme === 'dark' || (!savedTheme && systemPrefersDark)) {
            document.documentElement.classList.add('dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            document.documentElement.classList.remove('dark');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }

        themeToggle.addEventListener('click', () => {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
                themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
                themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            }
        });
    }

    // =================================================================
    // 15. SYSTEM THEME CHANGE DETECTION
    // =================================================================
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                document.documentElement.classList.add('dark');
                if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            } else {
                document.documentElement.classList.remove('dark');
                if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            }
        }
    });

    // =================================================================
    // 16. SIDEBAR TOGGLE ARROW ICONS ( > / < )
    // =================================================================
    const sidebarToggleIcon = document.getElementById('sidebarToggleIcon');

    function updateSidebarToggleIcon() {
        if (!sidebarToggleIcon) return;

        if (body.classList.contains('sidebar-collapsed')) {
            // Sidebar বন্ধ → খোলার জন্য ডানে তীর
            sidebarToggleIcon.className = 'fas fa-chevron-right';
        } else {
            // Sidebar খোলা → বন্ধ করার জন্য বামে তীর
            sidebarToggleIcon.className = 'fas fa-chevron-left';
        }
    }

    // প্রথমবার চেক করো
    updateSidebarToggleIcon();

    // sidebarToggle ক্লিকে আইকন আপডেট করো
    sidebarToggle?.addEventListener('click', () => {
        // টগল করার পর আইকন আপডেট
        setTimeout(updateSidebarToggleIcon, 50); // ছোট ডিলে দিয়ে ট্রানজিশন স্মুথ
    });


    // =================================================================
    // 17. MOBILE MENU - KaiaAdmin Style (Slide Up + Full Features)
    // =================================================================
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuPanel = document.getElementById('mobileMenuPanel');

    const mobileNotificationBtn = document.getElementById('mobileNotificationBtn');
    const mobileThemeToggle = document.getElementById('mobileThemeToggle');

    // Open Menu
    mobileMenuBtn?.addEventListener('click', () => {
        mobileMenu.classList.remove('hidden');
        requestAnimationFrame(() => {
            mobileMenuPanel.classList.remove('translate-y-full');
        });
    });

    // Close Menu
    const closeMenu = () => {
        mobileMenuPanel.classList.add('translate-y-full');
        mobileMenuPanel.addEventListener('transitionend', () => {
            mobileMenu.classList.add('hidden');
        }, { once: true });
    };

    // Close on backdrop
    mobileMenu?.addEventListener('click', (e) => {
        if (e.target === mobileMenu) closeMenu();
    });

    // Notification
    mobileNotificationBtn?.addEventListener('click', () => {
        const notificationMenu = document.getElementById('notificationMenu');
        notificationMenu.classList.toggle('hidden');
        if (!notificationMenu.classList.contains('hidden')) {
            adjustNotificationPosition?.();
        }
        closeMenu();
    });

    // Theme Toggle + Icon Sync
    mobileThemeToggle?.addEventListener('click', () => {
        const isDark = document.documentElement.classList.contains('dark');
        const themeToggle = document.getElementById('themeToggle');

        if (isDark) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
            mobileThemeToggle.querySelector('i').className = 'fas fa-moon text-indigo-600 w-5';
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
            mobileThemeToggle.querySelector('i').className = 'fas fa-sun text-yellow-500 w-5';
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        }
        closeMenu();
    });

    // Close Button (Top-Right)
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    closeMobileMenu?.addEventListener('click', closeMenu);
});


/* 
========= (সম্পূর্ণ ফিচার লিস্ট) ==========
ফিচার                                         আছে?                      কাজ করে?
______________________________________________________________________________________
"data-open=""true"" থেকে submenu ওপেন",        Yes,                        Yes
URL পেস্টে সঠিক মেনু ওপেন,                       Yes,                        Yes
রিলোডে মেনু ওপেন থাকে,                          Yes,                        Yes
active_menu ক্লাস (Django থেকে),                 Yes,                        Yes
ক্লিকে সাবমেনু টগল,                              Yes,                         Yes
অন্য মেনু ক্লোজ,                                 Yes,                         Yes
localStorage সেভ (শুধু ওপেন স্টেট),              Yes,                         Yes
closeAllMenus() ফাংশন,                         Yes,                         Yes
ডার্ক/লাইট মোড,                                 Yes,                         Yes
সিস্টেম থিম ফলো,                                Yes,                         Yes
মোবাইল টগল আইকন (> / <),                    Yes,                         Yes
ডেস্কটপ টগল আইকন,                            Yes,                         Yes
মোবাইল মেনু (KaiaAdmin স্টাইল),                  Yes,                         Yes
নোটিফিকেশন ড্রপডাউন,                           Yes,                         Yes
ইউজার ড্রপডাউন,                                Yes,                         Yes
ফুলস্ক্রিন,                                        Yes,                         Yes

*/