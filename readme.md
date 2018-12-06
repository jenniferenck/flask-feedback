**Further Study**

Make sure your registration and authentication logic is being handled in your models.py
Make sure that if there is already a user_id in the session, do not allow users to see the register or login forms
Add a 404 page when a user or feedback can not be found as well as a 401 page when users are not authenticated or not authorized.
Add a column to the users table called is_admin which is a boolean that defaults to false. If that user is an admin, they should be able to add, update and delete any feedback for any user as well as delete users.
Make sure that if any of your form submissions fail, you display helpful error messages to the user about what went wrong.
Tests! Having tests around authentication and authorization is a great way to save time compared to manually QA-ing your app.
Challenge Add functionality to reset a password. This will involve learning about sending emails (take a look at the Flask Mail module. You will need to use a transactional mail server to get this to work, gmail is an excellent option) and will require you to add a column to your users table to store a password reset token. HINT - here is how that data flow works
A user clicks a link and is taken to a form to input their email
If their email exists, send them an email with a link and a unique token in the query string (take a look at the built in secrets module and the token_urlsafe function. You will create this unique token and store it in the database
Once the user clicks on that link, take them to a form to reset their password (make sure that the unique token is valid before letting them access this form)
Once the form has been submitted, update the password in the database and delete the token created for that user
