//const crypto = require('crypto');

async function hash_salt_password(username, password) {
    // Create a salt using the username
    const salt = username + "extremelysecureextremely"; // Add a unique string to make the salt harder to guess

    // Combine the salt and the password
    const salted_password = salt + password;

    const encoder = new TextEncoder();
    const data = encoder.encode(salted_password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    return hashedPassword;
}

function generate_keys() {
    // Use tweetnacl to generate a public key

    return publicKeyBase64;
  }

async function login(event) {
    event.preventDefault();

    // User Input
    const username_input = document.querySelector('input[name="username"]');
    const password_input = document.querySelector('input[name="password"]');
    const public_key_input = document.querySelector('input[name="public_key"]');
    const username = username_input.value;
    const password = password_input.value;

    // Create a salt using the username
    const salt = username + "extremelysecureextremely";

    // Combine the salt and the password
    const saltedPassword = salt + password;

    // Hash Password
    const encoder = new TextEncoder();
    const data = encoder.encode(saltedPassword);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashedPassword = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    password_input.value = hashedPassword;

    // Key Generation
    const keyPair = nacl.box.keyPair();
    const publicKeyBase64 = btoa(String.fromCharCode.apply(null, keyPair.publicKey));
    const privateKeyBase64 = btoa(String.fromCharCode.apply(null, keyPair.secretKey));
    public_key_input.value = publicKeyBase64;
    localStorage.setItem('private_key', privateKeyBase64);

    event.target.submit();
}