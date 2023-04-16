async function hash_salt_password(event) {
    event.preventDefault();

    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const username = usernameInput.value;
    const password = passwordInput.value;

    // Create a salt using the username
    const salt = username + "extremelysecureextremely"; // Add a unique string to make the salt harder to guess

    // Combine the salt and the password
    const saltedPassword = salt + password;

    const encoder = new TextEncoder();
    const data = encoder.encode(saltedPassword);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    passwordInput.value = hashedPassword;

    event.target.submit();
    window.alert(passwordInput.value);
}