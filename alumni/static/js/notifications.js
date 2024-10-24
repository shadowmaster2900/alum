$(document).ready(function () {
    function fetchUnreadNotifications() {
        $.ajax({
            url: '/alumni/load_unread_notifications/',
            method: 'GET',
            success: function (data) {
                $('#notification-menu-content').html(html);
            },
        });
    }

    // Click event for the bell icon
    $('.notification-bell').click(function () {
        // Fetch and display unread notifications
        fetchUnreadNotifications();
    });

    // Click event for the "Mark as Read" link
    $('.mark-as-read-link').click(function (e) {
        e.preventDefault();
        var notificationId = $(this).closest('li').data('notification-id');

        // Perform the mark as read action (you can use AJAX here if needed)

        // Remove the notification from the menu
        $(this).closest('li').remove();
    });
});
