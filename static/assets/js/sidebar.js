// =================================================================
// 1. INITIALIZATION & DOM ELEMENTS + SUBMENU STATE
// =================================================================
document.addEventListener("DOMContentLoaded", () => {
    const menuGroups = document.querySelectorAll(".menu-group > button");
    const menuLinks = document.querySelectorAll(".sidebar-link");
    const overlay = document.getElementById("overlay");
    const body = document.body;

    const userBtn = document.getElementById("userBtn");
    const userMenu = document.getElementById("userMenu");
    const notificationBtn = document.getElementById('notificationBtn');
    const notificationMenu = document.getElementById('notificationMenu');
    const fullscreenToggle = document.getElementById('fullscreenToggle');
    const themeToggle = document.getElementById('themeToggle');

    // Mobile Toggle
    const sidebarToggleMobile = document.getElementById('sidebarToggleMobile');
    const sidebarToggleIconMobile = document.getElementById('sidebarToggleIconMobile');

    // Desktop Toggle
    const sidebarToggleDesktop = document.getElementById('sidebarToggleDesktop');
    const sidebarToggleIconDesktop = document.getElementById('sidebarToggleIconDesktop');

    // =================================================================
    // 2. INITIALIZE SUBMENU STATE ON PAGE LOAD (Fix Reload + URL Paste)
    // =================================================================
    // 1. Close all submenus first
    document.querySelectorAll(".submenu").forEach(s => s.classList.add("hidden"));
    document.querySelectorAll("[id^='arrow-']").forEach(a => a.classList.remove("rotate-90"));

    // 2. Open submenus based on Django data-open="true"
    document.querySelectorAll(".menu-group > button[data-open='true']").forEach(btn => {
        const menuId = btn.dataset.menu;
        const submenu = document.getElementById("submenu-" + menuId);
        const arrow = document.getElementById("arrow-" + menuId);
        if (submenu) submenu.classList.remove("hidden");
        if (arrow) arrow.classList.add("rotate-90");
    });

    // 3. Save current open state to localStorage
    const openMenus = [];
    document.querySelectorAll(".submenu:not(.hidden)").forEach(s => openMenus.push(s.id));
    localStorage.setItem("openMenus", JSON.stringify(openMenus));

    // =================================================================
    // 3. SIDEBAR TOGGLE (Mobile & Desktop)
    // =================================================================
    sidebarToggleMobile?.addEventListener('click', () => {
        body.classList.toggle("mobile-open");
        overlay?.classList.toggle("hidden");

        if (body.classList.contains("mobile-open")) {
            sidebarToggleIconMobile.className = 'fas fa-chevron-left text-slate-800 dark:text-slate-900 text-sm';
        } else {
            sidebarToggleIconMobile.className = 'fas fa-chevron-right text-slate-800 dark:text-slate-900 text-sm';
        }
    });

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

    if (window.innerWidth >= 900 && !body.classList.contains('sidebar-collapsed')) {
        sidebarToggleIconDesktop.className = 'fas fa-chevron-left text-slate-800 dark:text-slate-900 text-sm';
    }

    // =================================================================
    // 4. MOBILE OVERLAY CLOSE
    // =================================================================
    overlay?.addEventListener("click", () => {
        body.classList.remove("mobile-open");
        overlay.classList.add("hidden");
    });

    // =================================================================
    // 5. SUBMENU TOGGLE (Click on Group Button)
    // =================================================================
    menuGroups.forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            e.stopPropagation();

            // Expand sidebar if collapsed
            if (body.classList.contains("sidebar-collapsed")) {
                body.classList.remove("sidebar-collapsed");
                body.classList.add("sidebar-expanded");
                if (sidebarToggleIconDesktop) {
                    sidebarToggleIconDesktop.className = 'fas fa-chevron-left text-slate-800 dark:text-slate-900 text-sm';
                }
            }

            const menuId = btn.dataset.menu;
            const submenu = document.getElementById("submenu-" + menuId);
            const arrow = document.getElementById("arrow-" + menuId);
            if (!submenu) return;

            const isOpen = !submenu.classList.contains("hidden");

            // Close all other submenus
            document.querySelectorAll(".submenu").forEach(s => {
                if (s.id !== submenu.id) s.classList.add("hidden");
            });
            document.querySelectorAll("[id^='arrow-']").forEach(a => {
                if (a.id !== arrow.id) a.classList.remove("rotate-90");
            });

            // Toggle current
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
    // 6. LINK CLICK: Open parent only
    // =================================================================
    menuLinks.forEach(link => {
        link.addEventListener("click", () => {
            if (link.closest('.menu-group > button')) return;

            // Close all
            document.querySelectorAll(".submenu").forEach(s => s.classList.add("hidden"));
            document.querySelectorAll("[id^='arrow-']").forEach(a => a.classList.remove("rotate-90"));

            // Open parent
            let parent = link.closest('.submenu');
            while (parent) {
                parent.classList.remove("hidden");
                const btn = parent.previousElementSibling;
                if (btn) {
                    const arrow = btn.querySelector('[id^="arrow-"]');
                    if (arrow) arrow.classList.add("rotate-90");
                }
                parent = parent.parentElement?.closest('.submenu');
            }

            saveOpenMenus();
        });
    });

    // =================================================================
    // 7. USER DROPDOWN
    // =================================================================
    if (userBtn && userMenu) {
        userBtn.addEventListener("click", e => {
            e.stopPropagation();
            userMenu.classList.toggle("hidden");
            if (notificationMenu && !notificationMenu.classList.contains('hidden')) {
                notificationMenu.classList.add('hidden');
            }
        });
        document.addEventListener("click", e => {
            if (!userBtn.contains(e.target) && !userMenu.contains(e.target)) {
                userMenu.classList.add("hidden");
            }
        });
    }

    // =================================================================
    // 8. NOTIFICATION DROPDOWN
    // =================================================================
    if (notificationBtn && notificationMenu) {
        notificationBtn.addEventListener('click', e => {
            e.stopPropagation();
            const isOpening = notificationMenu.classList.contains('hidden');
            notificationMenu.classList.toggle('hidden');
            if (userMenu && !userMenu.classList.contains('hidden')) userMenu.classList.add('hidden');
            if (isOpening) adjustNotificationPosition?.();
        });
        document.addEventListener('click', e => {
            if (!notificationBtn.contains(e.target) && !notificationMenu.contains(e.target)) {
                notificationMenu.classList.add('hidden');
            }
        });
        window.addEventListener('resize', () => {
            if (!notificationMenu.classList.contains('hidden')) adjustNotificationPosition?.();
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
        } else if (isFullscreen) {
            notificationMenu.style.position = 'fixed';
            notificationMenu.style.top = '4rem';
            notificationMenu.style.right = '1rem';
            notificationMenu.style.zIndex = '9999';
        } else {
            notificationMenu.style.position = 'absolute';
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
    fullscreenToggle?.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(console.error);
        } else {
            document.exitFullscreen?.();
        }
    });

    // =================================================================
    // 10. SAVE OPEN MENUS
    // =================================================================
    function saveOpenMenus() {
        const open = [];
        document.querySelectorAll(".submenu:not(.hidden)").forEach(s => open.push(s.id));
        localStorage.setItem("openMenus", JSON.stringify(open));
    }

    // =================================================================
    // 11. THEME TOGGLE
    // =================================================================
    if (themeToggle) {
        const saved = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const isDark = saved === 'dark' || (!saved && prefersDark);

        if (isDark) {
            document.documentElement.classList.add('dark');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            document.documentElement.classList.remove('dark');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }

        themeToggle.addEventListener('click', () => {
            document.documentElement.classList.toggle('dark');
            const nowDark = document.documentElement.classList.contains('dark');
            localStorage.setItem('theme', nowDark ? 'dark' : 'light');
            themeToggle.innerHTML = nowDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            document.documentElement.classList.toggle('dark', e.matches);
            themeToggle.innerHTML = e.matches ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        }
    });

    // =================================================================
    // 12. MOBILE MENU
    // =================================================================
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuPanel = document.getElementById('mobileMenuPanel');
    const closeMobileMenu = document.getElementById('closeMobileMenu');
    const mobileNotificationBtn = document.getElementById('mobileNotificationBtn');
    const mobileThemeToggle = document.getElementById('mobileThemeToggle');

    mobileMenuBtn?.addEventListener('click', () => {
        mobileMenu.classList.remove('hidden');
        requestAnimationFrame(() => mobileMenuPanel.classList.remove('translate-y-full'));
    });

    const closeMenu = () => {
        mobileMenuPanel.classList.add('translate-y-full');
        mobileMenuPanel.addEventListener('transitionend', () => {
            mobileMenu.classList.add('hidden');
        }, { once: true });
    };

    closeMobileMenu?.addEventListener('click', closeMenu);
    mobileMenu?.addEventListener('click', e => { if (e.target === mobileMenu) closeMenu(); });
    mobileNotificationBtn?.addEventListener('click', () => { document.getElementById('notificationBtn')?.click(); closeMenu(); });
    mobileThemeToggle?.addEventListener('click', () => { themeToggle.click(); closeMenu(); });
});