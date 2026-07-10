I have completed most of my Django application, and everything works perfectly on desktop. However, I have one remaining issue with the mobile responsiveness that I want you to help me fix professionally.

### Current Problem

When a user logs into the application using a mobile device, the sidebar navigation (Dashboard, Users, Profile, Settings, etc.) is displayed directly on the screen instead of being hidden. This causes the sidebar to cover the main content, making it difficult or impossible to view the selected page properly.

On desktop, everything works perfectly, so I do **not** want the desktop layout to be changed.

### What I Want

I want the mobile navigation to behave similarly to the ChatGPT or Google Gemini mobile apps:

* On mobile devices, the sidebar should be hidden by default.
* A hamburger menu (☰) should appear in the top navigation bar.
* When the user taps the hamburger button, the sidebar should slide in from the left.
* The user should then be able to select any navigation item (Dashboard, Profile, Settings, etc.).
* After a navigation item is selected, the sidebar should automatically close, allowing the selected page to occupy the full screen.
* The user should still be able to reopen the sidebar at any time by tapping the hamburger button again.
* Optionally, when the sidebar is open, a dark overlay should appear over the rest of the page, and tapping outside the sidebar should close it.

### Important Requirements

* Do not change the desktop design because it already works correctly.
* Only improve the mobile responsiveness.
* Use Bootstrap 5 if possible, since the project already uses Bootstrap.
* Ensure the solution works smoothly on Android and iPhone devices.
* Keep the design modern, clean, and professional.
* Make sure the sidebar animation is smooth.
* The solution should be fully responsive and production-ready.

### Files I Will Provide

I will provide:

1. `sidebar.html`
2. `navbar.html`

Use only these files to implement the mobile sidebar functionality. If necessary, you may also suggest any minimal CSS or JavaScript changes required, but avoid changing the overall structure of the application.

The goal is to make the mobile experience feel polished and intuitive while preserving the existing desktop experience.


Now this is the navbars.html file 
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* Base Navbar Glassmorphism Theme */
    .modern-navbar {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(226, 232, 240, 0.8);
        padding: 0.75rem 1.5rem;
        font-family: 'Inter', sans-serif;
        z-index: 1050; /* Keeps navbar reliably layered over page content */
    }

    /* Universal Underline Link Reset */
    .modern-navbar a,
    .modern-navbar a:hover,
    .modern-navbar a:focus,
    .modern-nav-link,
    .modern-nav-link:hover,
    .notification-item,
    .notification-item:hover {
        text-decoration: none !important;
        outline: none;
    }

    .navbar-brand-modern {
        font-weight: 800;
        font-size: 1.3rem;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #4f46e5 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        transition: transform 0.2s;
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }

    .navbar-brand-modern:hover {
        transform: scale(1.02);
    }

    .modern-nav-link {
        color: #4a5568 !important;
        font-weight: 500;
        font-size: 0.95rem;
        padding: 0.5rem 1rem !important;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .modern-nav-link:hover {
        color: #4f46e5 !important;
        background-color: #f1f5f9;
    }

    .modern-nav-link i {
        font-size: 1.1rem;
        color: #64748b;
        transition: color 0.2s;
    }

    .modern-nav-link:hover i {
        color: #4f46e5;
    }

    /* Custom Destructive Danger State Link on Hover */
    .text-danger-hover:hover {
        background-color: #fef2f2 !important;
        color: #dc2626 !important;
    }

    /* Notification Bell Ring Animation */
    .notification-wrapper:hover i.fa-bell {
        animation: bell-ring 0.6s ease-in-out both;
    }

    @keyframes bell-ring {
        0%, 100% { transform: rotate(0); }
        20%, 60% { transform: rotate(15deg); }
        40%, 80% { transform: rotate(-15deg); }
    }

    .modern-badge {
        font-size: 0.65rem;
        padding: 0.25em 0.5em;
        transform: translate(15%, -15%) !important;
        border: 2px solid #ffffff;
    }

    /* Premium Modernized Dropdown Architecture */
    .modern-dropdown-menu {
        position: absolute;
        border: none !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12) !important;
        border: 1px solid #e2e8f0 !important;
        overflow: hidden;
        z-index: 1100;
        width: 360px;
        max-height: 480px;
    }

    .notification-header {
        background-color: #f8fafc;
        border-bottom: 1px solid #edf2f7;
    }

    .notification-item {
        border-bottom: 1px solid #f1f5f9;
        transition: background-color 0.2s;
        border-left: 3px solid transparent;
        white-space: normal !important; /* Permits multi-line text wrapper behavior */
    }

    .notification-item.unread-item {
        background-color: #eff6ff !important;
        border-left-color: #3b82f6;
    }

    .notification-item:hover {
        background-color: #f8fafc !important;
    }

    .notification-footer {
        background-color: #f8fafc;
        border-top: 1px solid #edf2f7;
    }

    .modern-toggler {
        border: none;
        padding: 0.5rem;
        border-radius: 8px;
        background-color: transparent;
    }
    .modern-toggler:focus {
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.2);
        outline: none;
    }

    /* ========================================================================= */
    /* RESPONSIVE LAYOUT ENGINE (Mobile, Tablet, Desktop Media Adjustments)      */
    /* ========================================================================= */
    
    @media (max-width: 991.98px) {
        .navbar-collapse {
            background: #ffffff;
            margin-top: 0.75rem;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }

        .navbar-nav {
            align-items: flex-start !important;
            width: 100%;
        }

        .nav-item {
            width: 100%;
        }

        .modern-nav-link {
            width: 100%;
            padding: 0.65rem 1rem !important;
        }

        /* Responsive scaling mechanism for mobile notification viewports */
        .modern-dropdown-menu {
            position: static !important; /* Allows layout flow alignment on mobile screens */
            width: 100% !important;
            max-width: 100% !important;
            box-shadow: none !important;
            border: 1px solid #cbd5e1 !important;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        .ms-lg-2 {
            margin-left: 0 !important;
            margin-top: 0.25rem;
        }
    }
</style>

<nav class="navbar navbar-expand-lg modern-navbar fixed-top shadow-sm">
    <div class="container-fluid">
        
        <a class="navbar-brand navbar-brand-modern" href="{% url 'dashboard:router' %}">
            <i class="fa-solid fa-graduation-cap" style="-webkit-text-fill-color: #4f46e5;"></i>
            <span>CETMS</span>
        </a>

        <button class="navbar-toggler modern-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ms-auto align-items-center gap-1">

                {% if user.is_authenticated %}

                    <li class="nav-item dropdown me-1 notification-wrapper">
                        <a class="nav-link modern-nav-link position-relative" href="#" id="notificationDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fa-regular fa-bell"></i>
                            <span class="d-lg-none fw-medium text-secondary">Notifications</span>
                            {% if navbar_notification_count > 0 %}
                                <span class="position-absolute top-0 start-50 translate-middle badge rounded-pill bg-danger modern-badge">
                                    {{ navbar_notification_count }}
                                </span>
                            {% endif %}
                        </a>

                        <div class="dropdown-menu dropdown-menu-end modern-dropdown-menu p-0 mt-2" id="notificationMenu" aria-labelledby="notificationDropdown" style="display: none;">
                            
                            <div class="d-flex justify-content-between align-items-center px-3 py-2.5 notification-header">
                                <span class="fw-bold text-dark" style="font-size: 0.95rem;">Notifications</span>
                                {% if navbar_notification_count > 0 %}
                                    <span class="badge bg-danger rounded-pill px-2.5 py-1" style="font-size: 0.75rem;">
                                        {{ navbar_notification_count }} New
                                    </span>
                                {% endif %}
                            </div>

                            <div style="max-height: 320px; overflow-y: auto;">
                                {% if navbar_notifications %}
                                    {% for notification in navbar_notifications %}
                                        <a href="{{ notification.url|default:'#' }}" class="dropdown-item py-3 notification-item {% if not notification.is_read %}unread-item{% endif %}">
                                            <div class="d-flex justify-content-between align-items-start mb-1">
                                                <strong class="text-dark text-wrap pe-2" style="font-size: 0.88rem; line-height: 1.3; display: block;">
                                                    {{ notification.title }}
                                                </strong>
                                                {% if not notification.is_read %}
                                                    <span class="spinner-grow spinner-grow-sm text-primary flex-shrink-0 mt-1" role="status" style="width: 8px; height: 8px;"></span>
                                                {% endif %}
                                            </div>
                                            <p class="text-muted text-wrap mb-1" style="font-size: 0.82rem; line-height: 1.4;">
                                                {{ notification.message|truncatechars:70 }}
                                            </p>
                                            <div class="d-flex align-items-center text-secondary" style="font-size: 0.75rem;">
                                                <i class="fa-regular fa-clock me-1 text-muted" style="font-size: 0.75rem;"></i>
                                                {{ notification.created_at|timesince }} ago
                                            </div>
                                        </a>
                                    {% endfor %}
                                {% else %}
                                    <div class="text-center py-5 px-4 text-muted">
                                        <div class="mb-2">
                                            <i class="fa-regular fa-bell-slash fa-2x" style="color: #cbd5e1;"></i>
                                        </div>
                                        <span class="small fw-medium">All caught up! No notifications.</span>
                                    </div>
                                {% endif %}
                            </div>

                            <div class="d-flex justify-content-between align-items-center px-3 py-2 notification-footer">
                                <a href="{% url 'notifications:mark_all_read' %}" class="btn btn-link p-0 text-success text-decoration-none small fw-semibold" style="font-size: 0.82rem;">
                                    <i class="fa-solid fa-check-double me-1"></i>Mark all read
                                </a>
                                <a href="{% url 'notifications:list' %}" class="btn btn-sm btn-primary px-3 rounded-3" style="font-size: 0.8rem; font-weight: 500;">
                                    View All
                                </a>
                            </div>
                        </div>
                    </li>

                    <li class="nav-item">
                        <a class="nav-link modern-nav-link" href="{% url 'accounts:profile' %}">
                            <i class="fa-regular fa-circle-user"></i>
                            <span class="fw-medium text-secondary">
                                {{ user.get_full_name|default:user.username }}
                            </span>
                        </a>
                    </li>

                    <li class="nav-item ms-lg-2">
                        <a class="nav-link modern-nav-link text-danger-hover" href="{% url 'accounts:logout' %}" style="border: 1px solid #f1f5f9;">
                            <i class="fa-solid fa-arrow-right-from-bracket text-danger"></i>
                            <span>Logout</span>
                        </a>
                    </li>

                {% else %}

                    <li class="nav-item">
                        <a class="nav-link modern-nav-link text-primary fw-semibold" href="{% url 'accounts:login' %}">
                            <i class="fa-solid fa-sign-in-alt"></i> <span>Login</span>
                        </a>
                    </li>

                {% endif %}

            </ul>
        </div>
    </div>
</nav>

<div style="margin-top: 75px;"></div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const dropTrigger = document.getElementById("notificationDropdown");
        const dropMenu = document.getElementById("notificationMenu");

        if (dropTrigger && dropMenu) {
            dropTrigger.addEventListener("click", function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                if (dropMenu.style.display === "block") {
                    dropMenu.style.display = "none";
                } else {
                    dropMenu.style.display = "block";
                }
            });

            // Close context menus when user clicks outside the interface target space
            document.addEventListener("click", function(e) {
                if (!dropTrigger.contains(e.target) && !dropMenu.contains(e.target)) {
                    dropMenu.style.display = "none";
                }
            });
        }
    });
</script>


and this is the sidebar.html file 

   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* Base Sidebar Reset & Layout Constraints */
    .modern-sidebar {
        background-color: #0f172a !important; /* Elegant slate deep dark */
        font-family: 'Inter', sans-serif;
        border-right: 1px solid #1e293b;
        z-index: 1000;
        padding: 0;
    }

    /* Universal Text Underline Removal Guarantee */
    .modern-sidebar a,
    .modern-sidebar a:hover,
    .modern-sidebar a:focus,
    .sidebar-nav-link,
    .sidebar-nav-link:hover {
        text-decoration: none !important;
        outline: none;
    }

    .sidebar-brand-wrapper {
        padding: 1.25rem 1.5rem;
        background: #020617;
        border-bottom: 1px solid #1e293b;
    }

    .sidebar-brand {
        font-weight: 800;
        font-size: 1.25rem;
        letter-spacing: 0.5px;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .sidebar-category-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 1.2px;
        color: #64748b !important;
        text-transform: uppercase;
        padding: 0.75rem 1.5rem 0.25rem 1.5rem;
    }

    .sidebar-nav-link {
        color: #94a3b8 !important;
        font-weight: 500;
        font-size: 0.88rem;
        padding: 0.65rem 1rem !important;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0.15rem 1rem;
        white-space: nowrap;
    }

    .sidebar-nav-link i {
        font-size: 1rem;
        width: 20px;
        text-align: center;
        color: #64748b;
        transition: color 0.2s ease-in-out;
    }

    /* Hover States (Underline-Free) */
    .sidebar-nav-link:hover {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.05);
    }

    .sidebar-nav-link:hover i {
        color: #818cf8;
    }

    /* Active Route Context Indicator Wrapper */
    .sidebar-nav-link.active-route {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        color: #818cf8 !important;
        font-weight: 600;
    }
    
    .sidebar-nav-link.active-route i {
        color: #818cf8;
    }

    /* ========================================================================= */
    /* RESPONSIVE ENGINE (Adaptive layout handling across Desktop / Tablet / Phone) */
    /* ========================================================================= */
    
    /* Desktop Viewports (Laptops, Monitors, Large Displays) */
    @media (min-width: 992px) {
        .modern-sidebar {
            height: 100vh;
            position: fixed;
            top: 0;
            left: 0;
            overflow-y: auto;
        }
        /* Custom Minimal Scrollbar for Fixed panel mode */
        .modern-sidebar::-webkit-scrollbar {
            width: 4px;
        }
        .modern-sidebar::-webkit-scrollbar-track {
            background: #0f172a;
        }
        .modern-sidebar::-webkit-scrollbar-thumb {
            background: #334155;
            border-radius: 4px;
        }
        .sidebar-nav-link.active-route {
            border-left: 3px solid #6366f1;
            border-radius: 0 8px 8px 0;
            margin-left: 0;
        }
    }

    /* Tablet and Mobile Screen Form Factors (Responsive Touch Bar Transition) */
    @media (max-width: 991.98px) {
        .modern-sidebar {
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
            position: sticky;
            top: 0;
            border-right: none;
            border-bottom: 1px solid #1e293b;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: row;
            align-items: center;
        }

        .sidebar-brand-wrapper {
            border-bottom: none;
            padding: 1rem 1.25rem;
            flex-shrink: 0;
        }

        .py-3 {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        /* Hide desktop sub-headers to preserve clean inline rhythm horizontal layout spacing */
        .sidebar-category-label {
            display: none !important;
        }

        .modern-sidebar .nav {
            flex-direction: row !important;
            align-items: center;
            padding: 0.5rem 1rem 0.5rem 0;
        }

        .sidebar-nav-link {
            margin: 0 0.35rem;
            padding: 0.5rem 0.85rem !important;
            font-size: 0.82rem;
            display: inline-flex;
        }

        /* Hide horizontal scrollbar bar on mobile engines to optimize visual space */
        .py-3::-webkit-scrollbar {
            display: none;
        }
        .py-3 {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        
        .sidebar-nav-link.active-route {
            border-bottom: 2px solid #6366f1;
            border-radius: 8px 8px 0 0;
        }
    }
</style>

<div class="col-12 col-lg-2 modern-sidebar shadow-lg">

    <div class="sidebar-brand-wrapper text-center">
        <h5 class="sidebar-brand m-0">
            <i class="fa-solid fa-layer-group" style="-webkit-text-fill-color: #818cf8;"></i>
            <span>CETMS</span>
        </h5>
    </div>

    <div class="py-3">
        <ul class="nav flex-column">

            <li class="nav-item">
                <a href="{% url 'dashboard:router' %}" class="sidebar-nav-link">
                    <i class="fa-solid fa-chart-pie"></i>
                    <span>Dashboard</span>
                </a>
            </li>

            {% if request.user.role == "SUPER_ADMIN" %}
                <li class="nav-item sidebar-category-label">
                    <small>Administration</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'accounts:user_list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-users-gear"></i>
                        <span>System Users</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'accounts:create_user' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-user-plus"></i>
                        <span>Create User</span>
                    </a>
                </li>
            {% endif %}

            {% if request.user.role == "SUPER_ADMIN" or request.user.role == "TRAINER" %}
                
                <li class="nav-item sidebar-category-label">
                    <small>Student Management</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'students:register' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-user-plus"></i>
                        <span>Register Student</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'students:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-user-graduate"></i>
                        <span>All Students</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'students:pending_approvals' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-user-clock"></i>
                        <span>Pending Approvals</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'students:approved_students' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-user-check"></i>
                        <span>Approved Students</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Lessons</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'lessons:lesson_list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-book-bookmark"></i>
                        <span>Lessons</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'lessons:create_lesson' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-circle-plus"></i>
                        <span>Create Lesson</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Assignments</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'assignments:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-file-invoice"></i>
                        <span>Assignments</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'assignments:create' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-square-plus"></i>
                        <span>Create Assignment</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'assignments:submissions' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-clipboard-list"></i>
                        <span>Submissions</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Logbook</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'logbook:create_entry' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-book-open-reader"></i>
                        <span>Create Logbook</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'logbook:daily_entries' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-list-check"></i>
                        <span>Logbook Entries</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'logbook:report' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-file-shield"></i>
                        <span>Logbook Reports</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Evaluations</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'evaluations:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-star-half-stroke"></i>
                        <span>Evaluations</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'evaluations:analytics' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-chart-line"></i>
                        <span>Analytics</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Attendance</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'attendance:dashboard' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-calendar-days"></i>
                        <span>Attendance</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Reports</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'reports:dashboard' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-chart-gantt"></i>
                        <span>Reports Dashboard</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'reports:student_reports' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-user-shield"></i>
                        <span>Student Reports</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'reports:attendance_reports' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-calendar-check"></i>
                        <span>Attendance Reports</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'reports:assignment_reports' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-file-prescription"></i>
                        <span>Assignment Reports</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'reports:analytics' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-chart-bar"></i>
                        <span>System Analytics</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Certification</small>
                </li>
                
                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-award"></i>
                        <span>Certificates</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-user-shield"></i>
                        <span>Certificate Verification</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-cloud-arrow-down"></i>
                        <span>Download Certificates</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-file-signature"></i>
                        <span>Recommendation Letters</span>
                    </a>
                </li>
            {% endif %}

            {% if request.user.role == "STUDENT" %}

                <li class="nav-item sidebar-category-label">
                    <small>Student Portal</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'students:dashboard' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-gauge-high"></i>
                        <span>My Dashboard</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'students:profile' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-address-card"></i>
                        <span>My Profile</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'lessons:lesson_list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-book-open"></i>
                        <span>My Lessons</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'assignments:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-file-pen"></i>
                        <span>My Assignments</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'assignments:submissions' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-cloud-arrow-up"></i>
                        <span>My Submissions</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'logbook:create_entry' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-book-journal-whills"></i>
                        <span>My Logbook</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'attendance:dashboard' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-calendar-check"></i>
                        <span>Attendance</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Reports</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'reports:student_reports' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-chart-simple"></i>
                        <span>My Reports</span>
                    </a>
                </li>

                <li class="nav-item sidebar-category-label">
                    <small>Certification</small>
                </li>

                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-certificate"></i>
                        <span>My Certificates</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-circle-check"></i>
                        <span>Certificate Verification</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-download"></i>
                        <span>Download Certificates</span>
                    </a>
                </li>

                <li class="nav-item">
                    <a href="{% url 'certificates:list' %}" class="sidebar-nav-link">
                        <i class="fa-solid fa-file-lines"></i>
                        <span>Recommendation Letters</span>
                    </a>
                </li>
            {% endif %}

        </ul>
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const currentPath = window.location.pathname;
        const sidebarLinks = document.querySelectorAll(".sidebar-nav-link");

        sidebarLinks.forEach(link => {
            const hrefAttribute = link.getAttribute("href");
            if (hrefAttribute && currentPath.includes(hrefAttribute) && hrefAttribute !== "/") {
                link.classList.add("active-route");
                const icon = link.querySelector("i");
                if (icon) {
                    icon.classList.remove("fa-regular");
                    icon.classList.add("fa-solid");
                }
            }
        });
    });
</script>

so correct and regive me the back here seperately 