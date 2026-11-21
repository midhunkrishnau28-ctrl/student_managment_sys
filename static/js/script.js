/**
 * ================================================================
 * STUDENT RECORD MANAGEMENT SYSTEM - JavaScript
 * Handles sidebar toggle, form validation, and delete confirmation
 * ================================================================
 */

document.addEventListener("DOMContentLoaded", function () {

    // -------------------- Sidebar Toggle --------------------
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebar = document.getElementById("sidebar");

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });

        // Close sidebar when clicking outside on mobile
        document.addEventListener("click", function (e) {
            if (window.innerWidth < 992 &&
                sidebar.classList.contains("show") &&
                !sidebar.contains(e.target) &&
                !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove("show");
            }
        });
    }

    // -------------------- Form Validation --------------------
    const addStudentForm = document.getElementById("addStudentForm");
    if (addStudentForm) {
        addStudentForm.addEventListener("submit", function (e) {
            if (!addStudentForm.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            addStudentForm.classList.add("was-validated");
        });
    }

    // -------------------- Delete from View Students Table --------------------
    const deleteButtons = document.querySelectorAll(".btn-delete");
    const deleteModal = document.getElementById("deleteModal");
    const deleteStudentName = document.getElementById("deleteStudentName");
    const deleteStudentId = document.getElementById("deleteStudentId");
    const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

    let studentIdToDelete = null;

    if (deleteModal) {
        const bsModal = new bootstrap.Modal(deleteModal);

        deleteButtons.forEach(function (btn) {
            btn.addEventListener("click", function () {
                studentIdToDelete = btn.getAttribute("data-id");
                const studentName = btn.getAttribute("data-name");

                if (deleteStudentName) deleteStudentName.textContent = studentName;
                if (deleteStudentId) deleteStudentId.textContent = studentIdToDelete;

                bsModal.show();
            });
        });

        if (confirmDeleteBtn) {
            confirmDeleteBtn.addEventListener("click", function () {
                if (!studentIdToDelete) return;

                fetch("/api/delete/" + encodeURIComponent(studentIdToDelete), {
                    method: "DELETE",
                    headers: { "Content-Type": "application/json" }
                })
                    .then(function (response) { return response.json(); })
                    .then(function (data) {
                        bsModal.hide();
                        if (data.success) {
                            // Remove the row from the table
                            const row = document.getElementById("row-" + studentIdToDelete);
                            if (row) {
                                row.style.transition = "opacity 0.4s";
                                row.style.opacity = "0";
                                setTimeout(function () {
                                    row.remove();
                                    // Update the total count in footer
                                    const tableBody = document.querySelector("#studentsTable tbody");
                                    const footer = document.querySelector(".card-footer strong");
                                    if (footer && tableBody) {
                                        footer.textContent = tableBody.children.length;
                                    }
                                    // If no rows left, reload
                                    if (tableBody && tableBody.children.length === 0) {
                                        location.reload();
                                    }
                                }, 400);
                            }
                            showAlert("success", data.message);
                        } else {
                            showAlert("danger", data.message);
                        }
                        studentIdToDelete = null;
                    })
                    .catch(function (err) {
                        bsModal.hide();
                        showAlert("danger", "An error occurred while deleting the student.");
                        console.error(err);
                    });
            });
        }
    }

    // -------------------- Auto-dismiss alerts --------------------
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) bsAlert.close();
        }, 5000);
    });

});


/**
 * Dynamically inject a Bootstrap alert at the top of the content area.
 */
function showAlert(type, message) {
    const wrapper = document.querySelector(".content-wrapper");
    if (!wrapper) return;

    const icon = type === "success" ? "check-circle-fill" :
                 type === "danger" ? "x-circle-fill" :
                 "exclamation-triangle-fill";

    const alertDiv = document.createElement("div");
    alertDiv.className = "alert alert-" + type + " alert-dismissible fade show";
    alertDiv.setAttribute("role", "alert");
    alertDiv.innerHTML =
        '<i class="bi bi-' + icon + ' me-2"></i>' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';

    wrapper.insertBefore(alertDiv, wrapper.firstChild);

    setTimeout(function () {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alertDiv);
        if (bsAlert) bsAlert.close();
    }, 5000);
}
