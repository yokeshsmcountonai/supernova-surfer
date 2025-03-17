$(document).on('keydown', function (event) {
    if (event.key === "Escape") {
        $(document).ready(function () {
            $('#myModal').modal('show');
            $('#passwordForm').on('submit', function (event) {
                event.preventDefault();
                const passwordInput = $('#password');
                const password = passwordInput.val();

                if (password === '123') {
                    const currentIP = window.location.hostname;
                    window.location.href = 'http://' + currentIP + ':8006/';
                } else {
                    alert("Sorry, your password is wrong");
                }
                $('#myModal').modal('hide');
            });
        });
    }
});



