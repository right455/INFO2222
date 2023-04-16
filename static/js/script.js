
function encrypt(message, private_key, public_key){
    const nonce = new Uint8Array(24); // Initialize an all-zero nonce
    public_key = nacl.util.decodeBase64(public_key);
    private_key = nacl.util.decodeBase64(private_key);

    const cipher_text = nacl.box(
        nacl.util.decodeUTF8(message),
        nonce,
        public_key,
        private_key
    );

    return cipher_text;
};

function decrypt(message, private_key, public_key){
    //console.log(message)
    message = message.split(",").map((value) => parseInt(value));
    message = new Uint8Array(message);
    
    const nonce = new Uint8Array(24); // Initialize an all-zero nonce
    public_key = nacl.util.decodeBase64(public_key);
    private_key = nacl.util.decodeBase64(private_key);

    //Get the decoded message
    let decoded_message = nacl.box.open(message, nonce, public_key, private_key);

    //Get the human readable message
    let plain_text = nacl.util.encodeUTF8(decoded_message)
    //console.log(plain_text)
    //return the plaintext
    return plain_text;
};

async function fetchPublicKey(recipient) {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: `/get_public_key/${recipient}`,
        method: "GET",
        dataType: "json",
        success: function (data) {
          resolve(data.public_key);
        },
        error: function () {
          console.log("Error fetching public key.");
          reject("Error fetching public key.");
        },
      });
    });
}

$(document).ready(function () {
$("form[action='/send_message']").on("submit", async function (event) {
    event.preventDefault();

    const recipient = $("#recipient").val();
    const message = $("#message").val();

    // Fetch the recipient's public key
    const public_key = await fetchPublicKey(recipient);

    // Encrypt the message using the public key
    //console.log(public_key);
    private_key = localStorage.getItem('private_key');
    const encryptedMessage = encrypt(message, private_key, public_key);
    console.log(encryptedMessage);
    // Update the message input with the encrypted message
    $("#message").val(encryptedMessage);

    // Submit the form
    event.target.submit();
});



});

$(document).ready(function() {
    $("#get-messages").click(function() {
        $.ajax({
            url: "/get_messages",
            method: "GET",
            dataType: "json", // Add this line to expect JSON data from the server
            success: function(data) {
                console.log("Received data:", data);

                let html = "";
                if (data && data.length > 0) {
                    const sender_public_key = data[data.length-1];
                    for (let i = 0; i < data.length - 1; i++) {
                        const encryptedMessage = data[i];
                        // Get the private key from local storage
                        const private_key = localStorage.getItem("private_key");
                        
                        // Get the sender's public key (you need to fetch it from the server or store it in a variable)
                        

                        // Decrypt the message
                        const decryptedMessage = decrypt(encryptedMessage, private_key, sender_public_key);

                        html += "<p>" + decryptedMessage + "</p>";
                    };
                } else {
                    html = "<p>No messages found.</p>";
                }
                $("#messages-container").html(html);
            },
            error: function() {
                console.log("Error fetching messages.");
            }
        });
    });
});