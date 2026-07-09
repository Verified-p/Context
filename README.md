<div class="col-md-2 bg-dark min-vh-100 p-0">

    <div class="text-white p-3">

        <h5 class="text-center">CETMS</h5>

        <hr>

        <ul class="nav flex-column">

            <!-- ================= DASHBOARD ================= -->

            <li class="nav-item mb-2">
                <a href="{% url 'dashboard:router' %}" class="nav-link text-white">
                    <i class="fa fa-gauge"></i>
                    Dashboard
                </a>
            </li>

            <!-- ========================================= -->
            <!-- SUPER ADMIN -->
            <!-- ========================================= -->

            {% if request.user.role == "SUPER_ADMIN" %}

            <li class="nav-item mt-2 mb-2 text-warning">
                <small>ADMINISTRATION</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'accounts:user_list' %}" class="nav-link text-white">
                    <i class="fa fa-users"></i>
                    System Users
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'accounts:create_user' %}" class="nav-link text-white">
                    <i class="fa fa-user-plus"></i>
                    Create User
                </a>
            </li>

            {% endif %}

            <!-- ========================================= -->
            <!-- ADMIN + TRAINER -->
            <!-- ========================================= -->

            {% if request.user.role == "SUPER_ADMIN" or request.user.role == "TRAINER" %}

            <li class="nav-item mt-3 mb-2 text-warning">
                <small>STUDENT MANAGEMENT</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'students:register' %}" class="nav-link text-white">
                    <i class="fa fa-user-plus"></i>
                    Register Student
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'students:list' %}" class="nav-link text-white">
                    <i class="fa fa-user-graduate"></i>
                    All Students
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'students:pending_approvals' %}" class="nav-link text-white">
                    <i class="fa fa-user-clock"></i>
                    Pending Approvals
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'students:approved_students' %}" class="nav-link text-white">
                    <i class="fa fa-user-check"></i>
                    Approved Students
                </a>
            </li>

            <!-- ========================================= -->
            <!-- LESSONS -->
            <!-- ========================================= -->

            <li class="nav-item mt-3 mb-2 text-warning">
                <small>LESSONS</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'lessons:lesson_list' %}" class="nav-link text-white">
                    <i class="fa fa-book"></i>
                    Lessons
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'lessons:create_lesson' %}" class="nav-link text-white">
                    <i class="fa fa-plus-circle"></i>
                    Create Lesson
                </a>
            </li>

            <!-- ========================================= -->
            <!-- ASSIGNMENTS -->
            <!-- ========================================= -->

            <li class="nav-item mt-3 mb-2 text-warning">
                <small>ASSIGNMENTS</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'assignments:list' %}" class="nav-link text-white">
                    <i class="fa fa-file-alt"></i>
                    Assignments
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'assignments:create' %}" class="nav-link text-white">
                    <i class="fa fa-plus-circle"></i>
                    Create Assignment
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'assignments:submissions' %}" class="nav-link text-white">
                    <i class="fa fa-clipboard-check"></i>
                    Submissions
                </a>
            </li>

            <!-- ========================================= -->
            <!-- LOGBOOK -->
            <!-- ========================================= -->

            <li class="nav-item mt-3 mb-2 text-warning">
                <small>LOGBOOK</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'logbook:create_entry' %}" class="nav-link text-white">
                    <i class="fa fa-book-open"></i>
                    Create Logbook
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'logbook:daily_entries' %}" class="nav-link text-white">
                    <i class="fa fa-list"></i>
                    Logbook Entries
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'logbook:report' %}" class="nav-link text-white">
                    <i class="fa fa-file-alt"></i>
                    Logbook Reports
                </a>
            </li>

            <!-- ========================================= -->
            <!-- EVALUATIONS -->
            <!-- ========================================= -->

            <li class="nav-item mt-3 mb-2 text-warning">
                <small>EVALUATIONS</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'evaluations:list' %}" class="nav-link text-white">
                    <i class="fa fa-star"></i>
                    Evaluations
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'evaluations:analytics' %}" class="nav-link text-white">
                    <i class="fa fa-chart-line"></i>
                    Analytics
                </a>
            </li>

            <!-- ========================================= -->
            <!-- ATTENDANCE -->
            <!-- ========================================= -->

            <li class="nav-item mt-3 mb-2 text-warning">
                <small>ATTENDANCE</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'attendance:dashboard' %}" class="nav-link text-white">
                    <i class="fa fa-calendar-check"></i>
                    Attendance
                </a>
            </li>
            <!-- ========================================= -->
<!-- REPORTS -->
<!-- ========================================= -->

<li class="nav-item mt-3 mb-2 text-warning">
    <small>REPORTS</small>
</li>

<li class="nav-item mb-2">
    <a href="{% url 'reports:dashboard' %}" class="nav-link text-white">
        <i class="fa fa-chart-pie"></i>
        Reports Dashboard
    </a>
</li>

<li class="nav-item mb-2">
    <a href="{% url 'reports:student_reports' %}" class="nav-link text-white">
        <i class="fa fa-user-graduate"></i>
        Student Reports
    </a>
</li>

<li class="nav-item mb-2">
    <a href="{% url 'reports:attendance_reports' %}" class="nav-link text-white">
        <i class="fa fa-calendar-check"></i>
        Attendance Reports
    </a>
</li>

<li class="nav-item mb-2">
    <a href="{% url 'reports:assignment_reports' %}" class="nav-link text-white">
        <i class="fa fa-file-alt"></i>
        Assignment Reports
    </a>
</li>

<li class="nav-item mb-2">
    <a href="{% url 'reports:analytics' %}" class="nav-link text-white">
        <i class="fa fa-chart-line"></i>
        System Analytics
    </a>
</li>
            <!-- ================= CERTIFICATES ================= -->
            <li class="nav-item mt-3 mb-2 text-warning">
                <small>CERTIFICATION</small>
            </li>
            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-certificate"></i>
                     Certificates
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                     <i class="fa fa-circle-check"></i>
                Certificate Verification
                 </a>
            </li>
            <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                <i class="fa fa-download"></i>
                Download Certificates
            </a>
        </li>

        <li class="nav-item mb-2">
            <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                <i class="fa fa-file-lines"></i>
                Recommendation Letters
            </a>
        </li>

            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-circle-check"></i>
                Certificate Verification
                 </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-certificate"></i>
                    Certificates
                </a>
            </li>

           <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-circle-check"></i>
                    Certificate Verification
                 </a>
            </li>

            {% endif %}

            <!-- ========================================= -->
            <!-- STUDENT -->
            <!-- ========================================= -->

            {% if request.user.role == "STUDENT" %}

            <li class="nav-item mt-2 mb-2 text-warning">
                <small>STUDENT PORTAL</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'students:dashboard' %}" class="nav-link text-white">
                    <i class="fa fa-gauge"></i>
                    My Dashboard
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'students:profile' %}" class="nav-link text-white">
                    <i class="fa fa-id-card"></i>
                    My Profile
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'lessons:lesson_list' %}" class="nav-link text-white">
                    <i class="fa fa-book-open"></i>
                    My Lessons
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'assignments:list' %}" class="nav-link text-white">
                    <i class="fa fa-file-alt"></i>
                    My Assignments
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'assignments:submissions' %}" class="nav-link text-white">
                    <i class="fa fa-upload"></i>
                    My Submissions
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'logbook:create_entry' %}" class="nav-link text-white">
                    <i class="fa fa-book-open"></i>
                    My Logbook
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'attendance:dashboard' %}" class="nav-link text-white">
                    <i class="fa fa-calendar-check"></i>
                    Attendance
                </a>
            </li>
            <!-- ========================================= -->
<!-- MY REPORTS -->
<!-- ========================================= -->

<li class="nav-item mt-3 mb-2 text-warning">
    <small>REPORTS</small>
</li>

<li class="nav-item mb-2">
    <a href="{% url 'reports:student_reports' %}" class="nav-link text-white">
        <i class="fa fa-chart-bar"></i>
        My Reports
    </a>
</li>

           <!-- ========================================= -->
            <!-- CERTIFICATION -->
            <!-- ========================================= -->

            <li class="nav-item mt-3 mb-2 text-warning">
                <small>CERTIFICATION</small>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-certificate"></i>
                    My Certificates
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-circle-check"></i>
                    Certificate Verification
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-download"></i>
                    Download Certificates
                </a>
            </li>

            <li class="nav-item mb-2">
                <a href="{% url 'certificates:list' %}" class="nav-link text-white">
                    <i class="fa fa-file-lines"></i>
                    Recommendation Letters
                </a>
            </li>

            {% endif %}

        </ul>

    </div>

<!-- </div> -->